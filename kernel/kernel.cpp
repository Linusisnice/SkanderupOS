extern "C" void kernel_main() {
    const char* message = "Hello from Kernel!";
    char* video_memory = (char*)0xb8000; // VGA text mode starts here

    for (int i = 0; message[i] != '\0'; ++i) {
        video_memory[i * 2] = message[i];
        video_memory[i * 2 + 1] = 0x07; // Light gray on black background
    }

    while (true) {
        // Infinite loop to keep the kernel running
    }
}
