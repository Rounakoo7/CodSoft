import java.util.HashMap;
import java.util.Scanner;
class Bank{
    private static HashMap<Integer, BankAccount> bankAccounts = new HashMap<>();
    public boolean addBankAccount(BankAccount account){
        if(bankAccounts.containsKey(account.getAccountNumber())){
            return false;
        }
        else{
            bankAccounts.put(account.getAccountNumber(), account);
            return true;
        }
    }
    public HashMap<Integer, BankAccount> getBankAccounts(){
        return bankAccounts;
    }
}
class BankAccount{
    private double balance;
    private int account_number;
    private int pin;
    public BankAccount(int account_number, int pin, double balance){
        this.account_number = account_number;
        this.pin = pin;
        this.balance = balance;
    }
    public boolean authenticate(int account_number, int pin){
        if((this.account_number == account_number) && (this.pin == pin)){
            return true;
        }
        else{
            return false;
        }
    }
    public int getAccountNumber(){
        return account_number;
    }
    public double getBalance(){
        return balance;
    }
    public void deposit(double amount){
        balance += amount;
    }
    public boolean withdraw(double amount){
        if (amount <= balance) {
            balance -= amount;
            return true;
        }
        return false;
    }
}
class ATM {
    private Bank bank;
    public ATM(Bank bank){
        this.bank = bank;
    }
    public void displayMenu(){
        System.out.println("ATM Interface:");
        System.out.println("1. Check Balance");
        System.out.println("2. Deposit");
        System.out.println("3. Withdraw");
        System.out.println("4. Exit");
    }
    public void run(){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Welcome to the ATM Interface.");
        while(true){
            System.out.print("Enter your Account Number: ");        
            int accountNumber = scanner.nextInt();
            if(bank.getBankAccounts().containsKey(accountNumber)){
                BankAccount account = bank.getBankAccounts().get(accountNumber);
                System.out.print("Enter your pin to continue: ");
                int pin = scanner.nextInt();
                if(account.authenticate(account.getAccountNumber(), pin)){
                    boolean flag = true;
                    while(flag){
                        displayMenu();
                        System.out.print("Select an option: ");
                        int choice = scanner.nextInt();
                        switch(choice){
                            case 1:
                                System.out.println("The current balance of your account with account number " + account.getAccountNumber() + " is Rs. " + account.getBalance());
                                break;
                            case 2:
                                System.out.print("Enter the amount to you want to deposit: ");
                                account.deposit(scanner.nextDouble());
                                System.out.println("Deposit successful. The current balance of your account with account number " + account.getAccountNumber() + " is Rs. " + account.getBalance());
                                break;
                            case 3:
                                System.out.print("Enter the amount to you want to withdraw: ");
                                if(account.withdraw(scanner.nextDouble())){
                                    System.out.println("Withdrawal successful. The current balance of your account with account number " + account.getAccountNumber() + " is Rs. " + account.getBalance());
                                } 
                                else{
                                    System.out.println("Insufficient balance!");
                                }
                                break;
                            case 4:
                                System.out.println("Thank you for using the ATM service.");
                                flag = false;
                                break;
                            default:
                                System.out.println("Invalid option. Please select a valid option.");
                        }
                    }
                }
                else{
                    System.out.println("Invalid Credentials! Exiting ...");
                }
            }
            else{
                System.out.println("Account not found!");
            } 
            System.out.print("Please enter (y) to check another Account Number, or enter any other key to terminate.");
            String choice = scanner.next();
            if(!choice.equals("y")){
                System.out.print("Exitting ATM interface ...");
                break;
            }
        }                    
        scanner.close();
    }
}
public class ATMInterface {
    public static void main(String[] args) {
        int[][] accountDetails = {{454541224, 1234, 1000}, {123456789, 3214, 100000}, {546524488, 1092, 0}, {404870203, 8024, 5000}, {210820037, 7365, 35000}};
        Bank bank = new Bank();
        for(int i = 0; i < accountDetails.length; i++){
            if(bank.addBankAccount(new BankAccount(accountDetails[i][0], accountDetails[i][1], accountDetails[i][2]))){
                System.out.println("Account added successfully.");
            }
            else{
                System.out.println("Account cannot be added as it already exists!");
            }
        }
        ATM atm = new ATM(bank);
        atm.run();       
    }
}
