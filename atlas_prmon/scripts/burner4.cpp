#include<thread>
#include <iostream>
#include <vector>
#include <chrono>
using namespace std;
void burn_cpu() {
    while (true) {}
}
int main() {
    int duration = 60;
    auto start = std::chrono::steady_clock::now();
    std::vector<std::thread> threads;
    while (true) {
        auto elapsed = std::chrono::steady_clock::now() - start;
        if (elapsed > std::chrono::seconds(30)) {
            threads.emplace_back(burn_cpu);  // add new runaway thread
        }
        if (elapsed > std::chrono::seconds(duration))
            break;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    for (auto &t : threads)
        t.detach();
    return 0;
}