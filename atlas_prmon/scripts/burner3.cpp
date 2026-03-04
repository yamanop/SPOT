#include<thread>
#include <iostream>
#include <vector>
#include <chrono>
using namespace std;

int main() {

    int memoryMB = 500;
    int duration = 60;

    vector<char> memory(memoryMB * 1024 * 1024);

    auto start = chrono::steady_clock::now();

    vector<vector<char>> leaks;

while (true) {
    auto elapsed = chrono::steady_clock::now() - start;

    if (elapsed > chrono::seconds(duration))
        break;

    leaks.push_back(vector<char>(10 * 1024 * 1024)); // +10MB per second

    for (auto &block : leaks) {
        block[0] = 1;
    }

    std::this_thread::sleep_for(chrono::seconds(1));
}

    return 0;
}