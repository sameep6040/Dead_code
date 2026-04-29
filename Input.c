#include <stdio.h>

int unusedFunction() {
    int temp = 100;
    return temp;
}

int helperFunction() {
    int a = 10;
    int b = 20;
    int result = a + b;
    int useless = 999;

    if (0) {
        int deadBranch = 50;
    }

    if (5 > 3) {
        result = result + 1;
    }

    while (0) {
        int deadLoop1 = 200;
    }

    while (10 < 2) {
        int deadLoop2 = 300;
    }

    int x = 5;
    x = 10;

    int i = 0;

    while (i < 5) {
        i = i + 1;

        if (i == 2) {
            break;
            int afterBreak = 111;
        }

        if (i == 3) {
            continue;
            int afterContinue = 222;
        }
    }

    return result;

    int afterReturn = 500;
}

int main() {
    int num1 = 10;
    int num2 = 20;
    int total = num1 + num2;

    int garbage = 777;

    helperFunction();

    if (10 < 2) {
        int neverRuns = 999;
    }

    while (1 && 0) {
        int impossibleLoop = 123;
    }

    

    return total;

    int unreachableMain = 1000;
}