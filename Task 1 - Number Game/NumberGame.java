import java.util.Random;
import java.util.Scanner;
public class NumberGame{
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        System.out.println("Welcome to the Number Game!");
        System.out.println("Guess a number betweeen 0 to 100. You have only 5 attempts per round. The quicker you guess the better the score will be. The final score will be shown after you finish all the rounds.");
        int score = 0;
        int rounds = 0;
        while(true){
            rounds++;
            int targetNumber = random.nextInt(100) + 1;
            int attempts = 0;
            int maxAttempts = 5;
            int flag = 0;
            while(attempts < maxAttempts){
                System.out.print("Enter your guess: ");
                int userGuess = scanner.nextInt();
                scanner.nextLine();
                attempts++;
                if(userGuess == targetNumber){
                    System.out.println("Congratulations! You guessed the number " + targetNumber + " in " + attempts + " attempts.");
                    score += (maxAttempts - attempts + 1) * 20;
                    flag = 1;
                    break;
                } 
                else if(userGuess < targetNumber) {
                    if(attempts == maxAttempts){
                        break;
                    }
                    System.out.println("The number you guessed is lower than the target number! Try again.");
                } else {
                    if(attempts == maxAttempts){
                        break;
                    }
                    System.out.println("The number you guessed is higher than the target number! Try again.");
                }
            }
            if((attempts == maxAttempts) && (flag == 0)){
                System.out.println("Sorry, you've run out of attempts. The correct number was " + targetNumber + ".");
            }
            System.out.print("Enter (y) if you want to play again, else enter any other key: ");
            String playAgainInput = scanner.nextLine();
            if(!playAgainInput.equals("y")){
                break;
            }
        }
        System.out.println("Game over! Your score is " + (score / rounds) + " out of 100.");
        scanner.close();
    }
}
