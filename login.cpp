#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;

// Define the structure of a basic hashmap (simple key-value store)
struct HashMap
{
    struct Node
    {
        string key;
        string value;
        Node *next;
    };

    Node *table[100]; // A simple array of linked lists for hash buckets

    // Constructor to initialize hash table
    HashMap()
    {
        for (int i = 0; i < 100; i++)
        {
            table[i] = nullptr;
        }
    }

    // Hash function to get the index based on the key (username)
    int hashFunction(const string &key)
    {
        int hash = 0;
        for (char c : key)
        {
            hash = (hash + c) % 100;
        }
        return hash;
    }

    // Insert a key-value pair into the hashmap
    void insert(const string &key, const string &value)
    {
        int index = hashFunction(key);
        Node *newNode = new Node{key, value, table[index]};
        table[index] = newNode;
    }

    // Search for a key in the hashmap and return the associated value (password)
    string search(const string &key)
    {
        int index = hashFunction(key);
        Node *current = table[index];
        while (current != nullptr)
        {
            if (current->key == key)
            {
                return current->value;
            }
            current = current->next;
        }
        return ""; // Return empty string if not found
    }

    // Save the credentials to a file
    void saveToFile(const string &filename)
    {
        ofstream file(filename, ios::app);
        for (int i = 0; i < 100; i++)
        {
            Node *current = table[i];
            while (current != nullptr)
            {
                file << current->key << " " << current->value << "\n";
                current = current->next;
            }
        }
    }

    // Load credentials from a file into the hashmap
    void loadFromFile(const string &filename)
    {
        ifstream file(filename);
        string username, password;
        while (file >> username >> password)
        {
            insert(username, password);
        }
    }
};

int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        cout << "Usage: ./main <action> <user_type> <username> <password>" << endl;
        return 1;
    }

    string action = argv[1];
    string userType = argv[2];
    string username = argv[3];
    string password = argv[4];

    // Determine the filename based on user type
    string filename = (userType == "Student") ? "Student.txt" : "Admin.txt";

    // Create an instance of the HashMap
    HashMap map;
    map.loadFromFile(filename); // Load existing credentials from the file

    if (action == "login")
    {
        // Check if the credentials are valid for login
        string storedPassword = map.search(username);
        if (storedPassword != "" && storedPassword == password)
        {
            cout << "Login successful!" << endl;
        }
        else
        {
            cout << "Invalid username or password." << endl;
        }
    }
    else if (action == "register")
    {
        // Register new user
        if (map.search(username) == "")
        {
            map.insert(username, password);
            map.saveToFile(filename); // Save the new credentials to the file
            cout << "Registration successful!" << endl;
        }
        else
        {
            cout << "Username already exists." << endl;
        }
    }
    else
    {
        cout << "Invalid action." << endl;
    }

    return 0;
}
