Option Explicit

Const ForReading = 1
Const ForWriting = 2

Dim filename, strOldText, strNewText
Dim objFSO, objFile, strText
Dim errMsg


If WScript.Arguments.Count = 3 Then
    filename = WScript.Arguments.Item(0)
    strOldText = WScript.Arguments.Item(1)
    strNewText = WScript.Arguments.Item(2)
Else
    errMsg = "Error in replace text: incorrect number of parameters. Usage: replacetext.vbs <filename> <strOldText> <strNewText>"
	WScript.StdErr.WriteLine(errMsg)
    Wscript.Quit 1
End If

Set objFSO = CreateObject("Scripting.FileSystemObject")

On Error Resume Next
	Set objFile = objFSO.OpenTextFile(filename, ForReading)
If Err.number > 0 then 
	errMsg = "Error in replace text: " & Err.Description & " " & filename
	WScript.Echo errMsg
	WScript.StdErr.WriteLine(errMsg)
    Wscript.Quit 1	
End If

strText = objFile.ReadAll
objFile.Close
strNewText = Replace(strText, strOldText, strNewText)

Set objFile = objFSO.OpenTextFile(filename, ForWriting)
objFile.WriteLine strNewText
objFile.Close

Wscript.Quit 0

