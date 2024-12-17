#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

// Structure to hold question data
struct Question {
    int id;
    string text;
    vector<string> options;  
    char correctOption;
    string concept;
    string difficulty; 
};

// Function to map string difficulty to a priority (lower priority value means higher priority)
int difficultyPriority(const string& difficulty) {
    if (difficulty == "easy") return 1;
    if (difficulty == "medium") return 2;
    if (difficulty == "hard") return 3;
    return 4; 
}

// PriorityQueue Class
class PriorityQueue {
public:
    Question data[1000];
    int size;

    PriorityQueue() : size(0) {}

    void insert(const Question& q) {
        data[size++] = q;
        int i = size - 1;
        while (i > 0 && difficultyPriority(data[(i - 1) / 2].difficulty) > difficultyPriority(data[i].difficulty)) {
            swap(data[i], data[(i - 1) / 2]);
            i = (i - 1) / 2;
        }
    }

    Question extractMin() {
        if (size == 0) return {};
        Question root = data[0];
        data[0] = data[--size];
        heapify(0);
        return root;
    }

    Question peek() {
        return size > 0 ? data[0] : Question();
    }

    bool isEmpty() {
        return size == 0;
    }

private:
    void heapify(int i) {
        int smallest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < size && difficultyPriority(data[left].difficulty) < difficultyPriority(data[smallest].difficulty))
            smallest = left;
        if (right < size && difficultyPriority(data[right].difficulty) < difficultyPriority(data[smallest].difficulty))
            smallest = right;

        if (smallest != i) {
            swap(data[i], data[smallest]);
            heapify(smallest);
        }
    }
};

// Linked List Class to track used question IDs
class UsedQuestions {
public:
    struct Node {
        int id;
        Node* next;

        Node(int id) : id(id), next(nullptr) {}
    };

    UsedQuestions() : head(nullptr) {}

    void insert(int id) {
        Node* newNode = new Node(id);
        newNode->next = head;
        head = newNode;
    }

    bool contains(int id) {
        Node* current = head;
        while (current) {
            if (current->id == id) return true;
            current = current->next;
        }
        return false;
    }

    ~UsedQuestions() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

private:
    Node* head;
};

// Quiz Class
class Quiz {
public:
    Quiz(const string& course, const string& studentName)
        : course(course), studentName(studentName), score(0) {
        loadQuestions();
    }

    void start() {
        if (pq.isEmpty()) {
            cout << "No questions available for this course." << endl;
            return;
        }

        askQuestions();
        saveScore();
    }

private:
    string course;
    string studentName;
    int score;
    PriorityQueue pq;
    UsedQuestions usedQuestions;

    void loadQuestions() {
        ifstream file("questions.csv");
        string line, word;

        while (getline(file, line)) {
            stringstream ss(line);
            Question q;

            try {
                getline(ss, word, ',');
                q.id = stoi(word);  

                getline(ss, q.text, ',');
                
                
                string optionsString;
                getline(ss, optionsString, ',');
                stringstream optionsStream(optionsString);
                string option;
                while (getline(optionsStream, option, '|')) {
                    q.options.push_back(option);
                }

                getline(ss, word, ',');
                q.correctOption = word[0];
                getline(ss, q.concept, ',');
                getline(ss, word, ',');
                q.difficulty = word;  
                getline(ss, word, ',');

                if (word == course) pq.insert(q);
            }
            catch (const std::invalid_argument& e) {
                cout << "Error parsing question ID: " << word << endl;
                continue;  
            }
        }

        file.close();
    }

    void askQuestions() {
        Question currentQuestion = pq.extractMin();

        while (true) {
            bool correct = askQuestion(currentQuestion);
            if (correct) {
                cout << "Correct!" << endl;
                score++;
            } else {
                cout << "Incorrect!" << endl;
            }

            char next;
            cout << "Do you want to continue? (Y/N): ";
            cin >> next;
            if (toupper(next) != 'Y') break;

            if (!pq.isEmpty()) {
                bool found = false;
                while (!pq.isEmpty() && !found) {
                    currentQuestion = pq.extractMin();
                    if (!usedQuestions.contains(currentQuestion.id)) {
                        usedQuestions.insert(currentQuestion.id);
                        found = true;
                    }
                }
            } else break;
        }
    }

    bool askQuestion(const Question& q) {
        cout << "\nQuestion: " << q.text << endl;
        for (int i = 0; i < q.options.size(); i++) {
            cout << char('A' + i) << ". " << q.options[i] << endl;
        }
        cout << "Your Answer: ";
        char answer;
        cin >> answer;
        return toupper(answer) == q.correctOption;
    }

    void saveScore() {
        ofstream file("student_scores.txt", ios::app);
        if (file.is_open()) {
            file << studentName << ", " << score << endl;
            file.close();
        } else {
            cout << "Error opening file to save score!" << endl;
        }

        cout << "\nQuiz Finished! Your Score: " << score << endl;
    }
};

// Main function
int main() {
    cout << "Welcome to the Student Dashboard!\n";
    cout << "Enter your name: ";
    string studentName;
    cin.ignore(); 
    getline(cin, studentName);

    cout << "Choose a course: PF, OOP, DSA\n";
    string course;
    cin >> course;

    for (auto& c : course) c = toupper(c);
    if (course == "PF" || course == "OOP" || course == "DSA") {
        Quiz quiz(course, studentName);
        quiz.start();
    } else {
        cout << "Invalid course selection." << endl;
    }

    return 0;
}
