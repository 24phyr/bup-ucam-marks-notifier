### BUP UCAM Automation Playground

This Userscript is designed for students of **Bangladesh University of Professionals (BUP)** to automate the calculation of In-Course marks on the UCAM portal. It eliminates the manual math of converting CTs, Mids, and Lab marks, providing a real-time summary of your standing.

#### Key Features

1.  **Automatic Mark Calculation**
    * Automatically sums up your total obtained marks.

2.  **Grade Target Dashboard (Collapsible)**
    * A clean, hidden-by-default dashboard that calculates exactly **how many marks you need in the Final Exam** to hit every GPA milestone.
    * Well its hidden because you wont care about your marks until the end of the semester. You will probably not need it before then :)
    * Shows you if a grade is Already secured, Reachable, or Impossible.

3.  **"What-If" Simulation Mode**
    * Missing a mark? Is a field showing `--`?
    * **Click on any empty (`--`) mark** to type in a predicted score!
    * The script effectively simulates your total result based on your prediction, allowing you to plan ahead before the official marks are even uploaded.

#### How to Use
1.  Install **`Tempermonkey`** extension in your browser and install the script from here https://greasyfork.org/en/scripts/561046-bup-ucam-playground
2.  Go to your BUP UCAM Exam Mark Summary page.
3.  Select your session and view a course.
4.  Scroll to the bottom of the marks table to see your **Total Obtained**.
5.  Click the green **"Show Grade Targets"** button to see your final exam requirements.
6.  Click any yellow-highlighted `--` cell to simulate a mark.