#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

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
};//QuestionNode

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
    }//addQuestion

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
    }//modifyQuestion

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
    }//deleteQuestion

    void displayQuestions() {
        QuestionNode* current = head;
        while (current) {
            printQuestion(current);
            current = current->next;
        }
    }//displayQuestions

    void printQuestion(QuestionNode* q) {
        cout << "ID: " << q->id << "\nText: " << q->text << "\nOptions: ";
        for (const auto& opt : q->options) {
            cout << opt << " ";
        }
        cout << "\nCorrect Answer: " << q->correctAnswer << "\nConcept: " << q->concept
             << "\nDifficulty: " << q->difficulty << "\nCourse: " << q->course << "\n" << endl;
    }//printQuestion

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

        if (!getline(ss, idStr, ',') || !getline(ss, text, ',') || !getline(ss, optionsStr, ',') ||
            !getline(ss, correctAnswer, ',') || !getline(ss, concept, ',') ||
            !getline(ss, difficulty, ',') || !getline(ss, course, ',')) {
            cout << "Warning: Skipping malformed line at line " << lineNumber << ": " << line << endl;
            continue;
        }

        try {
            int id = stoi(idStr);

            vector<string> options;
            stringstream optionsStream(optionsStr);
            string option;
            while (getline(optionsStream, option, '|')) {
                options.push_back(option);
            }

            addQuestion(id, text, options, correctAnswer, concept, difficulty, course);
        } catch (const invalid_argument& e) {
            cout << "Error: Invalid ID at line " << lineNumber << ": " << idStr << endl;
        } catch (const out_of_range& e) {
            cout << "Error: ID out of range at line " << lineNumber << ": " << idStr << endl;
        }
    }

    file.close();
    cout << "Questions loaded successfully from " << filename << endl;
}//loadQuestionsFromCSV

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
    }//writeQuestionsToFile
}; //QuestionList

int main() {
    QuestionList questionList;
    questionList.loadQuestionsFromCSV("questions.csv");
    questionList.displayQuestions();
    questionList.writeQuestionsToFile("questions.csv");

    return 0;
}
