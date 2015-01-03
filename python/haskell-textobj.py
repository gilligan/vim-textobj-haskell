import sys

def isImport(text):
    """
    isImport(text) returns True if text is an import statement
    """
    return text.startswith("import ")

def isComment(text):
    """
    isComment(text) returns True if text is a comment
    """
    return text.startswith("--")

def isTypeSignature(text):
    """
    isTypeSignature(text) returns True if text is a type signature
    """
    if isComment(text):
        return False
    words = text.strip().split(" ")
    return True if len(words) > 3 and words[1] == "::" else False

def isBinding(text):
    """
    isBinding(text) returns true if text looks like a top level binding
    """
    text = text.strip()
    if (isComment(text)
            or text.startswith("data")
            or text.startswith("type")
            or text.startswith("instance")
            or text.startswith("class")
            or indentLevel(text) != 0):
        return False
    return False if len(text.split("=")) < 2 else True

def getContentType(text):
    """
    getConentType(text) returns the type of the haskell content:
    import    -> 'i'
    comment   -> 'c'
    binding   -> 'b'
    typesig   -> 't'
    statement -> 's'
    """
    if isImport(text):
        return 'i'
    elif isComment(text):
        return 'c'
    elif isBinding(text) and indentLevel(text) == 0:
        return 'b'
    elif isTypeSignature(text):
        return 't'
    else:
        return 's'

def line(t):
    return t[0]
def type(t):
    return t[1]
def succ(x):
    return x + 1
def pred(x):
    return x - 1
def empty(x):
    return len(x) == 0
def lastLine(x):
    return (len(x)-1)

def splitWith(f, l):
    """
    splitWith(f, l) splits the list l where (f(l[i]) == False)
    returning ([left],[right])
    """
    left = []
    right = []
    i = 0
    while (i<len(l) and f(l[i])):
        left.append(l[i])
        i = i + 1
    return (left, l[i:])

def indentLevel(text):
    """
    indentLevel(text) returns the number of leadings spaces in text
    """
    stripped = text.strip()
    if (len(stripped) == 0 or stripped == '\n'):
        return 0
    i = 0
    while (i < len(text) and text[i].isspace()):
        i = i + 1
    return i

def findWith(content, index, cmpF, iterF):
    """
    findWith(c,i,f,g) tarverses c via the iteration function g starting
    at index i comparing elements with comparator function f returning
    a tuple (Success, index) where Success is True/False depending on
    whether an element was found or not.
    """
    i = index
    while (i >= 0 and i < len(content)):
        if cmpF(content[i]):
            return (True, i)
        i = iterF(i)
    return (False, i)

def getBindingRange(start, end, content):
    """
    getBindingRange(s,e,c) detects start and end of a haskell
    binding in content in the range (content[start] ... content[end])
    """
    if start == end or (end - start == 1):
        return (end, end)
    (found, lastStatement) = findWith(content, end, lambda x: indentLevel(x) > 0, pred)
    if lastStatement < start:
        return (start+1, start+1)
    return (start +1, lastStatement +1)

def setRetValue(res):
    start = res[0]
    end = res[1]
    startPos = [0, start, 1, 0]
    endPos = [0, end, 999, 0]
    vim.command("let g:haskell_textobj_ret="+str([startPos, endPos]))

def parse(l, content):
    taggedLines = zip([x for x in range(len(content))], map(getContentType, content))
    bindings = filter(lambda x : x[1] == 'b', taggedLines)
    (befores, afters) = splitWith(lambda x : line(x) < l, bindings)
    searchStart = line(befores[-1]) if (not empty(befores)) else (l if isBinding(content[l]) else None)
    searchEnd = lastLine(content) if empty(afters) else line(afters[0])
    bindingRange = getBindingRange(searchStart, searchEnd, content)
    setRetValue(bindingRange)
    return bindingRange

def selectHaskellBinding(lines, cursor):
    return parse(cursor, lines)
