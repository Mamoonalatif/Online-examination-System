#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

struct Question
{
    int id;
    string text;
    vector<string> options;
    string correctAnswer;
    string concept;
    string difficulty;

    Question(int id, string text, vector<string> options, string correctAnswer, string concept, string difficulty)
        : id(id), text(text), options(options), correctAnswer(correctAnswer), concept(concept), difficulty(difficulty) {}
};

void writeQuestionsToFile(const vector<Question> &questions, const string &filename)
{
    ofstream file(filename);
    if (!file.is_open())
    {
        cout << "Failed to open file for writing!" << endl;
        return;
    }

    file << "ID,Text,Options,CorrectAnswer,Concept,Difficulty\n";

    for (const auto &q : questions)
    {
        file << q.id << "," << q.text << ",";
        for (size_t i = 0; i < q.options.size(); ++i)
        {
            file << q.options[i];
            if (i != q.options.size() - 1)
                file << "|"; // Separate options with "|"
        }
        file << "," << q.correctAnswer << "," << q.concept << "," << q.difficulty << "\n";
    }

    file.close();
    cout << "Questions saved to file successfully!" << endl;
}

void loadQuestionsFromFile(vector<Question> &questions, const string &filename)
{
    ifstream file(filename);
    if (!file.is_open())
    {
        cout << "Failed to open file for reading!" << endl;
        return;
    }

    string line;
    getline(file, line);

    while (getline(file, line))
    {
        stringstream ss(line);
        string id_str, text, options_str, correctAnswer, concept, difficulty;
        vector<string> options;

        getline(ss, id_str, ',');
        getline(ss, text, ',');
        getline(ss, options_str, ',');
        getline(ss, correctAnswer, ',');
        getline(ss, concept, ',');
        getline(ss, difficulty);

        // Parse options
        stringstream options_ss(options_str);
        string option;
        while (getline(options_ss, option, '|'))
        {
            options.push_back(option);
        }

        int id = stoi(id_str);

        Question newQuestion(id, text, options, correctAnswer, concept, difficulty);
        questions.push_back(newQuestion);
    }

    file.close();
    cout << "Questions loaded from file successfully!" << endl;
}

void addQuestion(vector<Question> &questions, int id, const string &text, const vector<string> &options,
                 const string &correctAnswer, const string &concept, const string &difficulty)
{
    Question newQuestion(id, text, options, correctAnswer, concept, difficulty);
    questions.push_back(newQuestion);
    cout << "Question added successfully!" << endl;
}

void displayQuestions(const vector<Question> &questions)
{
    for (const auto &q : questions)
    {
        cout << "ID: " << q.id << "\nText: " << q.text << "\nOptions:\n";
        for (const auto &option : q.options)
        {
            cout << "  - " << option << "\n";
        }
        cout << "Correct Answer: " << q.correctAnswer << "\nConcept: " << q.concept
             << "\nDifficulty: " << q.difficulty << "\n\n";
    }
}

Question *findQuestionById(vector<Question> &questions, int id)
{
    for (auto &q : questions)
    {
        if (q.id == id)
        {
            return &q;
        }
    }
    return nullptr;
}

void updateQuestion(vector<Question> &questions, int id, const string &newText, const vector<string> &newOptions,
                    const string &newCorrectAnswer, const string &newConcept, const string &newDifficulty)
{
    Question *q = findQuestionById(questions, id);
    if (q)
    {
        q->text = newText;
        q->options = newOptions;
        q->correctAnswer = newCorrectAnswer;
        q->concept = newConcept;
        q->difficulty = newDifficulty;
        cout << "Question updated successfully!" << endl;
    }
    else
    {
        cout << "Question with ID " << id << " not found!" << endl;
    }
}

void deleteQuestion(vector<Question> &questions, int id)
{
    bool found = false;
    for (size_t i = 0; i < questions.size(); ++i)
    {
        if (questions[i].id == id)
        {
            for (size_t j = i; j < questions.size() - 1; ++j)
            {
                questions[j] = questions[j + 1];
            }
            questions.pop_back();
            cout << "Question deleted successfully!" << endl;
            found = true;
            break;
        }
    }
    if (!found)
    {
        cout << "Question with ID " << id << " not found!" << endl;
    }
}

int main()
{
    vector<Question> questions;

    loadQuestionsFromFile(questions, "questions.csv");

    // Adding DSA-related MCQs
    addQuestion(questions, 1, "What is the time complexity of Binary Search?", {"O(n)", "O(log n)", "O(n^2)", "O(1)"}, "O(log n)", "Binary Search", "Easy");
    addQuestion(questions, 2, "Which data structure is used to implement a queue?", {"Array", "Linked List", "Stack", "Heap"}, "Linked List", "Queue", "Medium");
    addQuestion(questions, 3, "What is the space complexity of Merge Sort?", {"O(n)", "O(log n)", "O(n log n)", "O(1)"}, "O(n)", "Merge Sort", "Hard");
    addQuestion(questions, 4, "Which algorithm is used to find the shortest path in a graph?", {"Breadth-First Search", "Depth-First Search", "Dijkstra's Algorithm", "QuickSort"}, "Dijkstra's Algorithm", "Graph Algorithms", "Hard");
    addQuestion(questions, 5, "What is the time complexity of QuickSort in the worst case?", {"O(n)", "O(n log n)", "O(n^2)", "O(log n)"}, "O(n^2)", "Sorting", "Hard");

    cout << "All questions:\n";
    displayQuestions(questions);

    updateQuestion(questions, 2, "Which data structure is commonly used to implement a queue?",
                   {"Array", "Linked List", "Circular Queue", "Heap"}, "Linked List", "Queue", "Medium");

    cout << "Updated questions:\n";
    displayQuestions(questions);

    deleteQuestion(questions, 1);

    cout << "Remaining questions:\n";
    displayQuestions(questions);

    writeQuestionsToFile(questions, "questions.csv");

    return 0;
}
