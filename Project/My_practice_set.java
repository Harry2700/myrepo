import java.util.Scanner;

public class My_practice_set {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();  // Input number
        int originalNumber = n;  // Store the original number
        int reverse = 0;  // Variable to store the reversed number

        // Palindrome check logic
        while (n > 0) {
            int a = n % 10;  // Get the last digit of n
            reverse = reverse * 10 + a;  // Append the digit to reverse
            n = n / 10;  // Remove the last digit from n
        }

        // Compare the reversed number with the original number
        if (originalNumber == reverse) {
            System.out.println("palindrome");
        } else {
            System.out.println("not palindrome");
        }

        sc.close();  // Close the scanner resource
    }
}
