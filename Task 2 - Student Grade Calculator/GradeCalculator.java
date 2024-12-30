import java.util.Scanner;
public class GradeCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Grade Calculator");
        System.out.print("Enter the number of subjects: ");
        int subjects = scanner.nextInt();
        int totalMarks = 0;
        for(int i = 1; i <= subjects; i++){
            System.out.print("Enter marks obtained in subject " + i + " out of 100: ");
            int currentMarks = scanner.nextInt();
            if((currentMarks >= 0) && (currentMarks <= 100)){ 
                totalMarks += currentMarks;
            }
            else{
                System.out.print("Invalid input! Exiting ..."); 
                scanner.close();
                return;       
            }
        }
        scanner.close();
        double averagePercentage = (double)(totalMarks / subjects);
        char grade;
        if(averagePercentage >= 90){
            grade = 'A';
        }
        else if(averagePercentage >= 80){
            grade = 'B';
        } 
        else if(averagePercentage >= 70){
            grade = 'C';
        } 
        else if(averagePercentage >= 60){
            grade = 'D';
        }
        else{
            grade = 'F';
        }
        System.out.println("Evaluating ...");
        System.out.println("Total Marks(out of " + (subjects * 100) + "): " + totalMarks);
        System.out.println("Average Percentage: " + averagePercentage + " %");
        System.out.println("Grade: " + grade);
    }
}
