import * as vscode from 'vscode';
import { open, load, DataType, close } from 'ffi-rs';

function sayhi () {
    // Open the user32 library
    open({
        library: "user32",
        path: "C:\\Windows\\System32\\user32.dll"
    });

    const r = load({
            library: 'user32',
            funcName: 'MessageBoxA',
            retType: DataType.I32,
            paramsType: [DataType.Void, DataType.String, DataType.String, DataType.I32],
                        paramsValue: [
                0, // null pointer for hWnd
                'Hello World from VS Code Extension!',
                'Extension Activated',
                0 // MB_OK
            ]
        });
}

export function activate(context: vscode.ExtensionContext) {

	sayhi();

	const disposable = vscode.commands.registerCommand('task2.helloWorld', () => {
		vscode.window.showInformationMessage('Hello World from Task2!');
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
