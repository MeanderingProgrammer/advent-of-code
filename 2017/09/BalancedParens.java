public class BalancedParens {

    private static final String open  = "([<{";
    private static final String close = ")]>}";

    public static void main(String[] args) {
        isBalanced("()[]<>{}");     // true 
        isBalanced("(<");           // false
        isBalanced("]}");           // false
        isBalanced("()<");          // false
        isBalanced("(][)");         // false
        isBalanced("{(X)[XY]}");    // true
    }

    private static boolean isBalanced(String input) {
        return isBalanced(input, "");
    }

    private static boolean isBalanced(String input, String stack) {
        if (input.isEmpty()) {
            return stack.isEmpty();
        } else {
            char first = input.charAt(0);
            if (isOpen(first)) {
                return isBalanced(input.substring(1), first + stack);
            } else if (isClose(first)) {
                return !stack.isEmpty() 
                    && isMatching(stack.charAt(0), first)
                    && isBalanced(input.substring(1), stack.substring(1));
            } else {
                return isBalanced(input.substring(1), stack);
            }
        }
    }

    private static boolean isOpen(char ch) {
        return open.indexOf(ch) != -1;
    }

    private static boolean isClose(char ch) {
        return close.indexOf(ch) != -1;
    }

    private static boolean isMatching(char chOpen, char chClose) {
        return open.indexOf(chOpen) == close.indexOf(chClose);
    }
}
