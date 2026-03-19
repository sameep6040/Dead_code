int calculateSum() {
    int a = 5;
    int b = 10;
    int result = a + b;
    int unused1 = 100;
    return result;
    int unreachable1 = 200;
}

int unusedFunction() {
    int x = 50;
    return x;
}

int main() {

    int num1 = 10;
    int num2 = 20;
    int total = num1 + num2;

    int garbage = 999;

    calculateSum();

    if(0) {
        int neverUsed = 500;
    }

    int i = 0;

    while(i < 3) {
        i = i + 1;
    }

    return total;

    int afterReturn = 1000;
}