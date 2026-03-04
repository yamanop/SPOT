#include <iostream>
#include <vector>
#include <chrono>
using namespace std;

int main() {

    int memoryMB = 500;
    int duration = 60;

    vector<char> memory(memoryMB * 1024 * 1024);

    auto start = chrono::steady_clock::now();

    while (true) {
        auto elapsed = chrono::steady_clock::now() - start;

        if (elapsed > chrono::seconds(60)) {
            memory.resize(1000 * 1024 * 1024); 
        }

        if (elapsed > chrono::seconds(duration))
            break;

        for (size_t i = 0; i < memory.size(); i++) {
            memory[i] = i % 256;
        }
    }

    return 0;
}