#include <iostream>
#include <fstream>
#include <string>
using namespace std;

struct HashMap
{   struct Node
    {
        string key, value;
        Node *next;
    };
    Node *table[10];

    HashMap() { fill(begin(table), end(table), nullptr); }

    int hashFunction(const string &key)
    {
        int hash = 0;
        for (char c : key)
            hash = (hash + c) % 100;
        return hash;
    }//hashFunction

    void insert(const string &key, const string &value)
    {
        int index = hashFunction(key);
        table[index] = new Node{key, value, table[index]};
    }//insert

    string search(const string &key)
    {
        int index = hashFunction(key);
        for (Node *current = table[index]; current; current = current->next)
            if (current->key == key)
                return current->value;
        return "";
    }//search

    void saveToFile(const string &filename)
    {
        ofstream file(filename, ios::app);
        for (int i = 0; i < 10; i++)
            for (Node *current = table[i]; current; current = current->next)
                file << current->key << " " << current->value << "\n";
    }//savetoFile

    void loadFromFile(const string &filename)
    {
        ifstream file(filename);
        string username, password;
        while (file >> username >> password)
            insert(username, password);
    }//loadfromfile
};

int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        cout << "Usage: ./main <action> <user_type> <username> <password>\n";
        return 1;
    }

    string action = argv[1], userType = argv[2];
    string username = argv[3], password = argv[4];
    string filename = (userType == "Student") ? "Student.txt" : "Admin.txt";

    HashMap map;
    map.loadFromFile(filename);

    if (action == "login")
    {
        string storedPassword = map.search(username);
        cout << (storedPassword == password ? "Login successful!" : "Invalid username or password.") << endl;
    }
    else if (action == "register")
    {
        if (map.search(username).empty())
        {
            map.insert(username, password);
            map.saveToFile(filename);
            cout << "Registration successful!" << endl;
        }
        else
            cout << "Username already exists." << endl;
    }
    else
    {
        cout << "Invalid action." << endl;
    }

    return 0;
}
