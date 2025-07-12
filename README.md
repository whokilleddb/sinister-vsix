# Sinister VSIx - Experimenting with C++, Node JS and Electron till I lose my mind

![](https://pyxis.nymag.com/v1/imgs/595/75c/02221a3d3580bab3d23fc672e9909c4890-11-sinister-six.2x.h473.w710.jpg)

This blog serves as a journal of sorts to record the research process which went behind backdooring electron applications and all the problems along the way. Before we talk about the main crux of the blog, it is important to have some context and get some terminologies right.

## Introduction 

The main inspiration for this research comes from the following [MDSec Blog](https://www.mdsec.co.uk/2023/08/leveraging-vscode-extensions-for-initial-access/). The blog talks about using [Node Native Addons](https://nodejs.org/api/addons.html) to get reverse shells back. 

This blog post got me thinking - _Can we make this more legit? Can we backdoor a legitimate looking extension with this technique?_

However, that was a far off question. I had no idea how VSCode/Node/Electron worked, so I set the following goal for myself:

> Task #1: Write a node addon which pops `Hello World` message box when loaded 

----
### Task #1

We take a look at the [following example](https://nodejs.org/api/addons.html#hello-world) from the Node Addon Docs.

The very first example we are shown is: 

```cc
// hello.cc
#include <node.h>

namespace demo {

using v8::FunctionCallbackInfo;
using v8::Isolate;
using v8::Local;
using v8::NewStringType;
using v8::Object;
using v8::String;
using v8::Value;

void Method(const FunctionCallbackInfo<Value>& args) {
  Isolate* isolate = args.GetIsolate();
  args.GetReturnValue().Set(String::NewFromUtf8(
      isolate, "world", NewStringType::kNormal).ToLocalChecked());
}

void Initialize(Local<Object> exports) {
  NODE_SET_METHOD(exports, "hello", Method);
}

NODE_MODULE(NODE_GYP_MODULE_NAME, Initialize)

}  // namespace demo 
```

Technically, this _should_ work as a starting point. Infact, lets write a simple program ourselves to test this out. 

```cc
// hello_world.cc
#include <Windows.h>
#include <node.h>

namespace hello_world {

    using v8::FunctionCallbackInfo;
    using v8::Isolate;
    using v8::Local;
    using v8::Object;
    using v8::String;
    using v8::Value;

    // Hello World shellcode taken from: https://gist.github.com/kkent030315/b508e56a5cb0e3577908484fa4978f12
    void runshellcode() {
        unsigned char shellcode[] =  "\x48\x83\xEC\x28\x48\x83\xE4\xF0\x48\x8D\x15\x66\x00\x00\x00"
                            "\x48\x8D\x0D\x52\x00\x00\x00\xE8\x9E\x00\x00\x00\x4C\x8B\xF8"
                            "\x48\x8D\x0D\x5D\x00\x00\x00\xFF\xD0\x48\x8D\x15\x5F\x00\x00"
                            "\x00\x48\x8D\x0D\x4D\x00\x00\x00\xE8\x7F\x00\x00\x00\x4D\x33"
                            "\xC9\x4C\x8D\x05\x61\x00\x00\x00\x48\x8D\x15\x4E\x00\x00\x00"
                            "\x48\x33\xC9\xFF\xD0\x48\x8D\x15\x56\x00\x00\x00\x48\x8D\x0D"
                            "\x0A\x00\x00\x00\xE8\x56\x00\x00\x00\x48\x33\xC9\xFF\xD0\x4B"
                            "\x45\x52\x4E\x45\x4C\x33\x32\x2E\x44\x4C\x4C\x00\x4C\x6F\x61"
                            "\x64\x4C\x69\x62\x72\x61\x72\x79\x41\x00\x55\x53\x45\x52\x33"
                            "\x32\x2E\x44\x4C\x4C\x00\x4D\x65\x73\x73\x61\x67\x65\x42\x6F"
                            "\x78\x41\x00\x48\x65\x6C\x6C\x6F\x20\x77\x6F\x72\x6C\x64\x00"
                            "\x4D\x65\x73\x73\x61\x67\x65\x00\x45\x78\x69\x74\x50\x72\x6F"
                            "\x63\x65\x73\x73\x00\x48\x83\xEC\x28\x65\x4C\x8B\x04\x25\x60"
                            "\x00\x00\x00\x4D\x8B\x40\x18\x4D\x8D\x60\x10\x4D\x8B\x04\x24"
                            "\xFC\x49\x8B\x78\x60\x48\x8B\xF1\xAC\x84\xC0\x74\x26\x8A\x27"
                            "\x80\xFC\x61\x7C\x03\x80\xEC\x20\x3A\xE0\x75\x08\x48\xFF\xC7"
                            "\x48\xFF\xC7\xEB\xE5\x4D\x8B\x00\x4D\x3B\xC4\x75\xD6\x48\x33"
                            "\xC0\xE9\xA7\x00\x00\x00\x49\x8B\x58\x30\x44\x8B\x4B\x3C\x4C"
                            "\x03\xCB\x49\x81\xC1\x88\x00\x00\x00\x45\x8B\x29\x4D\x85\xED"
                            "\x75\x08\x48\x33\xC0\xE9\x85\x00\x00\x00\x4E\x8D\x04\x2B\x45"
                            "\x8B\x71\x04\x4D\x03\xF5\x41\x8B\x48\x18\x45\x8B\x50\x20\x4C"
                            "\x03\xD3\xFF\xC9\x4D\x8D\x0C\x8A\x41\x8B\x39\x48\x03\xFB\x48"
                            "\x8B\xF2\xA6\x75\x08\x8A\x06\x84\xC0\x74\x09\xEB\xF5\xE2\xE6"
                            "\x48\x33\xC0\xEB\x4E\x45\x8B\x48\x24\x4C\x03\xCB\x66\x41\x8B"
                            "\x0C\x49\x45\x8B\x48\x1C\x4C\x03\xCB\x41\x8B\x04\x89\x49\x3B"
                            "\xC5\x7C\x2F\x49\x3B\xC6\x73\x2A\x48\x8D\x34\x18\x48\x8D\x7C"
                            "\x24\x30\x4C\x8B\xE7\xA4\x80\x3E\x2E\x75\xFA\xA4\xC7\x07\x44"
                            "\x4C\x4C\x00\x49\x8B\xCC\x41\xFF\xD7\x49\x8B\xCC\x48\x8B\xD6"
                            "\xE9\x14\xFF\xFF\xFF\x48\x03\xC3\x48\x83\xC4\x28\xC3";
        printf("shellcode size: %d\n", sizeof(shellcode));
        DWORD flOldProtect;
        VirtualProtect(shellcode, sizeof(shellcode), PAGE_EXECUTE_READWRITE, &flOldProtect);
        (*(void (*)())&shellcode)();
    }


    void ShowMessageBox(const FunctionCallbackInfo<Value>& args) {
        runshellcode();
    }

    void Initialize(Local<Object> exports) {
        NODE_SET_METHOD(exports, "showMessageBox", ShowMessageBox);
    }

    NODE_MODULE(NODE_GYP_MODULE_NAME, Initialize)

}  // namespace hello_world
```

Now to compile this, we first need to install `node-gyp`. I will not got into the details of how to setup the pre-requisites for `node-gyp` itself - just follow the instructions [here](https://github.com/nodejs/node-gyp).

Once you have all the pre-requisites setup, install node-gyp with:

```bash
npm install -g node-gyp
```

Next, we need to create a `binding.gyp` file. Consider this as a sort of config file for `node-gyp` itself. Its is actually pretty simple:

```json
{
  "targets": [
    {
      "target_name": "hello_world",
      "sources": [ "hello_world.cc" ],
    }
  ]
}
```

Now to create an addon we need to run the following from a x64 Native Tools Command Prompt for Visual Studio:

```bash
node-gyp configure
node-gyp build
```

If everything is okay, you should see a `gyp info ok` at the end of the compilation process and you should have a `build\Release\hello_world.node` file.

Now, we can verify that our addon works by using the following script:

```js
// index.js
const addon = require('./build/Release/hello_world.node');
addon.showMessageBox();
```

Running the following script as follows gives us a sweet sweet Message Box pop-up:

```bash
node index.js
```

![](./imgs/task1.png)

So with this, our **Test#1** has been concluded successfully! Time to move onto the next part.

---

## Wait - why not use FFI?

At this point, some keen readers might be asking: _Why do we need all this C++ stuff? Why not use something like [node-ffi](https://github.com/node-ffi/node-ffi)?_

And the answer is: I AM STUPID

I had tried playing with things like [ffi-napi](https://www.npmjs.com/package/ffi-napi) and [node-ffi](https://github.com/node-ffi/node-ffi) libraries but could not get them to work due to some problems with electrons - but during writing this blog, I dipped my toe in it again and this time, I got it working! 

![](https://i.imgur.com/XJyemeI.jpeg)

So, time for another task -

> Task #2: Create a VS Code extension and pop a hello world message box from it using FFI! 

----

## Task #2 

First, we need to create a VS Code extension. For this, we would be using the [following guide](https://code.visualstudio.com/api/get-started/your-first-extension). The guide requires you to install `yo` and `generator-code`.

Once you have installed the packages, create a 

```bash
yo code --skip-cache --ask-answered --open --extensionType ts --pkgManager npm  --extensionDisplayName Task2 --quick task2
```

This creates a base folder called `task2` which contains the template for a basic extension. The main source code for the extension is stored in `src/extension.ts`. Hitting F5 with the `extension.ts` focused pops up another Visual Stuido Code. Bringing up the Visual Studio Prompt and searching for `Hello World` title and selecting it would pop up a message in the Debug Console of the original window - showing that our extension works!

![](./imgs/task2_1.png)

