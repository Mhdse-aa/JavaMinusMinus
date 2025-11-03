import my.pkg;

class Test extends Base implements Runnable {
    public static void main(String[] args) {
        int x = 1_234;
        int y = 0;
        char c = '\n';
        String s = "Hello \"World\" \\n Done";
        boolean flag = true || false && !false;

        if (x >= 10 && y != 0) {
            x = x + 1;
        } else {
            y = y - 1;
        }

        for (int i = 0; i < 5; i = i + 1) {
            // loop body
            s = s + "!";
        }

        while (x < 20) {
            x = x * 2;
        }

        return;
    }
}
