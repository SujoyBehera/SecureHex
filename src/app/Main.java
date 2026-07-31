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
        if(name.isEmpty()){
            System.out.println("Name cannot be empty");
        }
        System.out.print("Enter Your Email:");
        String email = scanner.nextLine().trim().toLowerCase();
        if(email.isEmpty()){
            System.out.println("Email cannot be empty");
        }
        System.out.print("Enter Your Master Password:");
        String masterpassword = scanner.nextLine().trim();
        if(masterpassword.isEmpty()){
            System.out.println("Master Password cannot be empty");
        }
        //Confirmation registration
        System.out.println("====================================");
        System.out.println("Registration Successful!!!");
        System.out.println("Welcome " + name);
        System.out.println("Email:" + email);
        System.out.println("current credentials:" + totalcredentials);
        System.out.println("====================================");
        System.out.println("Do you want to login?");
        System.out.println("1.YES 2.EXIT:");
        int choice = scanner.nextInt();
        scanner.nextLine();
        if(choice == 1) {
            //Login Screen
            System.out.print("Enter the registered email:");
            String useremail = scanner.nextLine().trim().toLowerCase();
            System.out.print("Enter your master password:");
            String userpassword = scanner.nextLine().trim();
            if (useremail.equals(email)) {
                if(userpassword.equals(masterpassword)){
                    System.out.println("Your Email and Master Password is correct");
                    System.out.println("Login Successful!!");
                    login = true;
                    System.out.println("Login Status: " + login);
                }
                else {
                    System.out.print("Incorrect password.");
                }
            }
            else{
                System.out.print("Email not found.");
            }
        }
        else{
            System.out.println("GoodBye!");
        }
        scanner.close();

    }
}


