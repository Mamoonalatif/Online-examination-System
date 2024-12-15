#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

// Node for the doubly linked list to store questions
struct QuestionNode {
    int id;
    string text;
    vector<string> options;
    string correctAnswer;
    string concept;
    string difficulty;
    string course;
    QuestionNode* next;
    QuestionNode* prev;

    QuestionNode(int id, const string& text, const vector<string>& options,
                 const string& correctAnswer, const string& concept, const string& difficulty, const string& course)
        : id(id), text(text), options(options), correctAnswer(correctAnswer),
          concept(concept), difficulty(difficulty), course(course), next(nullptr), prev(nullptr) {}
};

// Doubly Linked List to manage questions
class QuestionList {
private:
    QuestionNode* head;
    QuestionNode* tail;

    QuestionNode* findQuestionById(int id) {
        QuestionNode* current = head;
        while (current) {
            if (current->id == id)
                return current;
            current = current->next;
        }
        return nullptr;
    }

public:
    QuestionList() : head(nullptr), tail(nullptr) {}

    void addQuestion(int id, const string& text, const vector<string>& options,
                 const string& correctAnswer, const string& concept, const string& difficulty, const string& course) {
    if (findQuestionById(id)) {
        cout << "Warning: Question with ID " << id << " already exists.\n";
        return;
    }
    QuestionNode* newNode = new QuestionNode(id, text, options, correctAnswer, concept, difficulty, course);

    if (!head) {
        head = tail = newNode;
    } else {
        tail->next = newNode;
        newNode->prev = tail;
        tail = newNode;
    }
}


    void modifyQuestion(int id, const string& newText, const vector<string>& newOptions,
                        const string& newCorrectAnswer, const string& newConcept, const string& newDifficulty, const string& newCourse) {
        QuestionNode* q = findQuestionById(id);
        if (q) {
            q->text = newText;
            q->options = newOptions;
            q->correctAnswer = newCorrectAnswer;
            q->concept = newConcept;
            q->difficulty = newDifficulty;
            q->course = newCourse;
            cout << "Question with ID " << id << " has been modified successfully.\n";
        } else {
            cout << "Question with ID " << id << " not found.\n";
        }
    }

    void deleteQuestion(int id) {
        QuestionNode* q = findQuestionById(id);
        if (q) {
            if (q->prev)
                q->prev->next = q->next;
            else
                head = q->next;

            if (q->next)
                q->next->prev = q->prev;
            else
                tail = q->prev;

            delete q;
            cout << "Question with ID " << id << " has been deleted successfully.\n";
        } else {
            cout << "Question with ID " << id << " not found.\n";
        }
    }

    void displayQuestions() {
        QuestionNode* current = head;
        while (current) {
            printQuestion(current);
            current = current->next;
        }
    }

    void printQuestion(QuestionNode* q) {
        cout << "ID: " << q->id << "\nText: " << q->text << "\nOptions: ";
        for (const auto& opt : q->options) {
            cout << opt << " ";
        }
        cout << "\nCorrect Answer: " << q->correctAnswer << "\nConcept: " << q->concept
             << "\nDifficulty: " << q->difficulty << "\nCourse: " << q->course << "\n" << endl;
    }

    void loadQuestionsFromCSV(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "Error: Could not open file " << filename << endl;
        return;
    }

    string line;
    int lineNumber = 0;

    while (getline(file, line)) {
        lineNumber++;

        if (line.empty()) {
            cout << "Warning: Skipping empty line at line " << lineNumber << endl;
            continue;
        }

        stringstream ss(line);
        string idStr, text, optionsStr, correctAnswer, concept, difficulty, course;

        // Parse fields
        if (!getline(ss, idStr, ',') || !getline(ss, text, ',') || !getline(ss, optionsStr, ',') ||
            !getline(ss, correctAnswer, ',') || !getline(ss, concept, ',') ||
            !getline(ss, difficulty, ',') || !getline(ss, course, ',')) {
            cout << "Warning: Skipping malformed line at line " << lineNumber << ": " << line << endl;
            continue;
        }

        // Validate and convert ID
        try {
            int id = stoi(idStr);

            // Parse options
            vector<string> options;
            stringstream optionsStream(optionsStr);
            string option;
            while (getline(optionsStream, option, '|')) {
                options.push_back(option);
            }

            // Add question to the list
            addQuestion(id, text, options, correctAnswer, concept, difficulty, course);
        } catch (const invalid_argument& e) {
            cout << "Error: Invalid ID at line " << lineNumber << ": " << idStr << endl;
        } catch (const out_of_range& e) {
            cout << "Error: ID out of range at line " << lineNumber << ": " << idStr << endl;
        }
    }

    file.close();
    cout << "Questions loaded successfully from " << filename << endl;
}


    void writeQuestionsToFile(const string& filename) {
        ofstream file(filename);
        if (!file.is_open()) {
            cout << "Error: Could not open file " << filename << " for writing." << endl;
            return;
        }
  file << "ID,Text,Options,CorrectAnswer,Concept,Difficulty\n";
        QuestionNode* current = head;
        while (current) {
            file << current->id << "," << current->text << ",";

            for (size_t i = 0; i < current->options.size(); ++i) {
                file << current->options[i];
                if (i < current->options.size() - 1)
                    file << "|";
            }

            file << "," << current->correctAnswer << "," << current->concept << ","
                 << current->difficulty << "," << current->course << "\n";

            current = current->next;
        }

        file.close();
        cout << "Questions written successfully to " << filename << endl;
    }
};

int main() {
    QuestionList questionList;
 // Load questions from CSV file
    questionList.loadQuestionsFromCSV("questions.csv");

    // Adding 10 questions for DSA
    questionList.addQuestion(1, "What is the time complexity of Binary Search?", {"O(n)", "O(log n)", "O(n^2)", "O(1)"}, "O(log n)", "Binary Search", "Easy", "DSA");
    questionList.addQuestion(2, "Which data structure is used in BFS?", {"Stack", "Queue", "Heap", "Graph"}, "Queue", "Graph Traversal", "Medium", "DSA");
    questionList.addQuestion(3, "What is the height of a complete binary tree with N nodes?", {"log N", "N", "log(N+1)-1", "N-1"}, "log(N+1)-1", "Binary Trees", "Hard", "DSA");
    questionList.addQuestion(4, "Which algorithm is used for finding the shortest path in a graph?", {"DFS", "Dijkstra's", "Prim's", "Kruskal's"}, "Dijkstra's", "Graph Algorithms", "Medium", "DSA");
    questionList.addQuestion(5, "What is a max heap?", {"Complete binary tree", "Tree with max root", "Tree with min root", "Heap without duplicates"}, "Tree with max root", "Heaps", "Easy", "DSA");
    questionList.addQuestion(6, "What is the time complexity of quicksort in the worst case?", {"O(n log n)", "O(n^2)", "O(n)", "O(log n)"}, "O(n^2)", "Sorting", "Hard", "DSA");
    questionList.addQuestion(7, "Which data structure supports LIFO?", {"Queue", "Deque", "Stack", "Heap"}, "Stack", "Stacks", "Easy", "DSA");
    questionList.addQuestion(8, "Which traversal is used to print a binary search tree in sorted order?", {"Inorder", "Preorder", "Postorder", "Level-order"}, "Inorder", "Tree Traversal", "Medium", "DSA");
    questionList.addQuestion(9, "Which of the following is not a stable sorting algorithm?", {"Bubble Sort", "Selection Sort", "Merge Sort", "Insertion Sort"}, "Selection Sort", "Sorting", "Hard", "DSA");
    questionList.addQuestion(10, "Which data structure is used in recursion?", {"Queue", "Heap", "Stack", "Graph"}, "Stack", "Recursion", "Easy", "DSA");

    // Adding 10 questions for OOP
    questionList.addQuestion(11, "What is a class in OOP?", {"Object", "Blueprint", "Method", "Variable"}, "Blueprint", "Basics", "Easy", "OOP");
    questionList.addQuestion(12, "Which principle does inheritance follow?", {"Encapsulation", "Reusability", "Abstraction", "Polymorphism"}, "Reusability", "Inheritance", "Easy", "OOP");
    questionList.addQuestion(13, "What is polymorphism?", {"Overloading", "Overriding", "Both", "None"}, "Both", "Polymorphism", "Medium", "OOP");
    questionList.addQuestion(14, "What is encapsulation?", {"Hiding data", "Inheritance", "Method Overloading", "Abstraction"}, "Hiding data", "Basics", "Easy", "OOP");
    questionList.addQuestion(15, "What is function overriding?", {"Same function name, different classes", "Same name, same parameters", "Different parameters", "None"}, "Same name, same parameters", "Polymorphism", "Medium", "OOP");
    questionList.addQuestion(16, "Which keyword is used to inherit a class?", {"virtual", "private", "public", "protected"}, "public", "Inheritance", "Easy", "OOP");
    questionList.addQuestion(17, "What does 'this' pointer represent?", {"Current object", "Base class", "Derived class", "None"}, "Current object", "Pointers", "Medium", "OOP");
    questionList.addQuestion(18, "Which operator is used for dynamic memory allocation in C++?", {"new", "malloc", "alloc", "calloc"}, "new", "Dynamic Memory", "Easy", "OOP");
    questionList.addQuestion(19, "Which of the following supports multiple inheritance?", {"C++", "Java", "Python", "C#"}, "C++", "Inheritance", "Hard", "OOP");
    questionList.addQuestion(20, "What is the access specifier of private members in inheritance?", {"Accessible", "Not accessible", "Hidden", "Read-only"}, "Not accessible", "Inheritance", "Medium", "OOP");

    // Adding 10 questions for PF
    questionList.addQuestion(21, "What is the size of an int in C++?", {"2 bytes", "4 bytes", "8 bytes", "16 bytes"}, "4 bytes", "Data Types", "Easy", "PF");
    questionList.addQuestion(22, "Which loop executes at least once?", {"for", "while", "do-while", "none"}, "do-while", "Loops", "Easy", "PF");
    questionList.addQuestion(23, "What is the correct syntax for an if statement?", {"if condition then", "if (condition)", "if condition", "condition then"}, "if (condition)", "Conditions", "Easy", "PF");
    questionList.addQuestion(24, "What is the value of 5 % 2?", {"1", "2", "0", "None"}, "1", "Operators", "Easy", "PF");
    questionList.addQuestion(25, "Which header file is required for input/output?", {"iostream", "stdlib", "stdio", "math"}, "iostream", "Headers", "Easy", "PF");
    questionList.addQuestion(26, "Which data type is used to store decimals?", {"int", "float", "char", "bool"}, "float", "Data Types", "Easy", "PF");
    questionList.addQuestion(27, "What does \"return 0\" signify?", {"Success", "Error", "Infinite loop", "None"}, "Success", "Basics", "Easy", "PF");
    questionList.addQuestion(28, "What is the output of 4+5*3?", {"15", "27", "19", "None"}, "19", "Operators", "Medium", "PF");
    questionList.addQuestion(29, "Which operator is used for logical AND?", {"&&", "||", "==", "!"}, "&&", "Operators", "Easy", "PF");
    questionList.addQuestion(30, "What is the default value of an uninitialized int?", {"0", "garbage", "null", "undefined"}, "garbage", "Variables", "Medium", "PF");

    // Display all questions
    questionList.displayQuestions();
   // Write questions to file
    questionList.writeQuestionsToFile("questions.csv");

    return 0;
}
