
#include <iostream>
#include <omp.h>
#include <vector>
using namespace std;

void saxpy(int n, float a, float* x, float* y) {
    for (int i = 0; i < n; i++) {
        y[i] = a * x[i] + y[i];
    }
}

int main() {
    int n = 1000;
    float a = 2.0;
    vector<float> x(n, 1.0), y(n, 2.0);

    saxpy(n, a, x.data(), y.data());

    // Print first 10 elements as correctness check
    for (int i = 0; i < 10; i++) {
        cout << y[i] << " ";
    }
    cout << endl;
    return 0;
}
