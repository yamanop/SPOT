#include <iostream>
#include <vector>
#include <chrono>
using namespace std;

int main(int argc, char* argv[]) {
    int memoryMB = 500;
    int duration = 60;

    vector<char> memory(memoryMB * 1024 * 1024);

    auto start = chrono::steady_clock::now();
    while (chrono::steady_clock::now() - start < chrono::seconds(duration)) {
        for (size_t i = 0; i < memory.size(); i++) {
            memory[i] = i % 256;
        }
    }

    return 0;
}
