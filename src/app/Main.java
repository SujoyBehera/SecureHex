package app;

import java.util.Scanner;
public class Main {
    public static void main(String[] args){
        //Variables
        String appname ="SecureHex";
        int totalcredentials = 0;
        boolean login = false;
        //Welcome screen
        System.out.println("====================================");
        System.out.println("           "+appname);
        System.out.println("Secure Credential Management System");
        System.out.println("====================================");
        System.out.println("Login status:" + login);

        //User Registration
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter Your Name:");
        String  name = scanner.nextLine().trim();
        while(name.isEmpty()){
            System.out.println("Name cannot be empty");
            System.out.print("Enter Your Name:");
            name = scanner.nextLine().trim();

        }
        System.out.print("Enter Your Email:");
        String email = scanner.nextLine().trim().toLowerCase();
        while( email.isEmpty() || !email.contains("@")){
            if(email.isEmpty()){
                System.out.println("Email cannot be empty");
            }
            else{
                System.out.println("Invalid Email");
            }
            System.out.print("Enter Your Email:");
            email = scanner.nextLine().trim().toLowerCase();

        }

        System.out.print("Enter Your Master Password:");
        String masterpassword = scanner.nextLine().trim();

        while(masterpassword.length() < 8 || masterpassword.isEmpty()){
            if(masterpassword.isEmpty()){
                System.out.println("Password cannot be empty");
            }
            else{
                System.out.println("Password must contain at least 8 characters");
            }
            System.out.print("Enter Your Master Password:");
            masterpassword = scanner.nextLine().trim();

        }
        //Confirmation registration
        System.out.println("====================================");
        System.out.println("Registration Successful!!");
        System.out.println("Account Created Successfully");
        System.out.println("Welcome " + name);
        System.out.println("Email:" + email);
        System.out.println("current credentials:" + totalcredentials);
        System.out.println("====================================");
        System.out.println("Do you want to login?");
        System.out.println("1.YES 2.EXIT:");
        int choice = scanner.nextInt();
        scanner.nextLine();
        //Login
        if(choice == 1) {
            //Login Screen
            System.out.println("Number of attempts are 3");
            for(int i = 1; i<=3; i++){
                System.out.println("attempt:" + i);
                System.out.print("Enter the registered email:");
                String useremail = scanner.nextLine().trim().toLowerCase();
                System.out.print("Enter your master password:");
                String userpassword = scanner.nextLine().trim();
                if (useremail.equals(email) && userpassword.equals(masterpassword)) {
                    System.out.println("Your Email and Master Password is correct");
                    System.out.println("Login Successful!!");
                    login = true;
                    System.out.println("Login Status: " + login);
                    break;
                }
                else {
                    System.out.print("Invalid Credentials");
                    if (i==3){
                        System.out.println("Maximum login attempts reached.");
                        System.out.println("Account Locked!");
                    }
                }
            }
        }
        else if (choice == 2){
            System.out.println("GoodBye!");
        }
        else{
            System.out.println("Invalid Input");
        }
        scanner.close();

    }
}


