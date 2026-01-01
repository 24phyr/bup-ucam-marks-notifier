    // ==UserScript==
    // @name         BUP UCAM Playground
    // @namespace    http://tampermonkey.net/
    // @version      1.1
    // @description  Calculates In-Course marks and guide you to achieve better result.
    // @author       mdtiTAHSIN
    // @match        https://ucam.bup.edu.bd/miu/result/StudentExamMarkSummary.aspx*
    // @grant        none
    // @license      MIT
    // ==/UserScript==
     
    (function() {
        'use strict';
     
        const TABLE_ID_PARTIAL = 'ExamMarkSummaryDetails';
        const RESULT_ROW_ID = 'userscript_calc_row';
        const PREDICTION_ID = 'userscript_prediction_card';
     
        // Grading Scale
        const GRADING_SCALE = [
            { grade: 'A+', point: '4.00', min: 80 },
            { grade: 'A', point: '3.75', min: 75 },
            { grade: 'A-', point: '3.50', min: 70 },
            { grade: 'B+', point: '3.25', min: 65 },
            { grade: 'B', point: '3.00', min: 60 },
            { grade: 'B-', point: '2.75', min: 55 },
            { grade: 'C+', point: '2.50', min: 50 },
            { grade: 'C', point: '2.25', min: 45 },
            { grade: 'D', point: '2.00', min: 40 }
        ];
     
        function parseMark(text) {
            if (!text) return 0;
            text = text.trim();
            if (text === '--' || text === '' || text.toLowerCase().includes('absent')) return 0;
            return parseFloat(text) || 0;
        }
     
        // --- 1. Grade Predictor UI ---
        function renderGradePredictor(targetTable, obtainedInCourse, isTheory) {
            const container = targetTable.closest('.card-body') || targetTable.parentElement;
            let wrapper = document.getElementById(PREDICTION_ID);
     
            if (!wrapper) {
                wrapper = document.createElement('div');
                wrapper.id = PREDICTION_ID;
                wrapper.style.marginTop = '15px';
                wrapper.style.maxWidth = '500px';
     
                const toggleBtn = document.createElement('button');
                toggleBtn.id = 'userscript_toggle_btn';
                toggleBtn.innerText = "Show Grade Targets";
                Object.assign(toggleBtn.style, {
                    backgroundColor: '#198754', color: 'white', border: 'none',
                    padding: '8px 15px', borderRadius: '5px', fontSize: '13px',
                    cursor: 'pointer', fontWeight: 'bold', display: 'flex', gap: '5px'
                });
     
                const contentDiv = document.createElement('div');
                contentDiv.id = 'userscript_prediction_content';
                contentDiv.style.display = 'none';
                contentDiv.style.marginTop = '10px';
                contentDiv.style.padding = '10px';
                contentDiv.style.border = '1px solid #d1e7dd';
                contentDiv.style.borderRadius = '5px';
                contentDiv.style.backgroundColor = '#f8fdfa';
     
                toggleBtn.onclick = (e) => {
                    e.preventDefault();
                    if (contentDiv.style.display === 'none') {
                        contentDiv.style.display = 'block';
                        toggleBtn.innerText = "Hide Grade Targets";
                        toggleBtn.style.backgroundColor = '#dc3545';
                    } else {
                        contentDiv.style.display = 'none';
                        toggleBtn.innerText = "Show Grade Targets";
                        toggleBtn.style.backgroundColor = '#198754';
                    }
                };
     
                wrapper.appendChild(toggleBtn);
                wrapper.appendChild(contentDiv);
                container.appendChild(wrapper);
            }
     
            const contentDiv = wrapper.querySelector('#userscript_prediction_content');
     
            const maxFinalMark = isTheory ? 100 : 40;
            const headerText = isTheory
                ? "Final Exam Targets (Paper mark out of 100)"
                : "Final Exam Targets (Paper mark out of 40)";
     
            let tbodyRows = '';
            GRADING_SCALE.forEach((tier) => {
                let gap = tier.min - obtainedInCourse;
                let requiredPaperMark = isTheory ? gap * 2 : gap;
     
                let statusText = '', rowStyle = 'border-bottom: 1px solid #eee;', statusColor = '#333';
     
                if (gap <= 0) {
                    statusText = "Done ✅";
                    rowStyle += 'background-color: #d1e7dd; color: #0f5132; font-weight: bold;'; statusColor = '#0f5132';
                } else if (requiredPaperMark > maxFinalMark) {
                    statusText = "-"; statusColor = '#ccc'; rowStyle += 'color: #aaa;';
                } else {
                    statusText = `${requiredPaperMark.toFixed(2)}`; statusColor = '#000';
                }
     
                tbodyRows += `<tr style="${rowStyle}">
                    <td style="padding: 4px;">${tier.grade}</td>
                    <td style="padding: 4px; text-align: center;">${tier.point}</td>
                    <td style="padding: 4px; text-align: center; color: ${statusColor}; font-weight: bold;">${statusText}</td>
                </tr>`;
            });
     
            contentDiv.innerHTML = `<div style="font-weight: bold; color: #0f5132; margin-bottom: 8px; border-bottom: 1px solid #ccc; padding-bottom: 5px; font-size: 13px;">${headerText}</div>
            <table style="width:100%; border-collapse:collapse; font-size:12px;">
                <thead><tr style="background-color: #eee; color: #333;"><th style="padding:5px;">Grade</th><th style="padding:5px; text-align:center;">GPA</th><th style="padding:5px; text-align:center;">Need</th></tr></thead>
                <tbody>${tbodyRows}</tbody>
            </table>`;
        }
     
        // --- 2. Recalculation Engine ---
        function updateCalculations(table) {
            const rows = Array.from(table.querySelectorAll('tbody tr')).filter(tr => !tr.querySelector('th') && tr.id !== RESULT_ROW_ID);
            const rowText = table.innerText.toLowerCase();
            const isTheory = (rowText.includes('class test') && rowText.includes('mid term'));
     
            let cts = [], mid = {o:0, t:0}, assign = {o:0, t:0}, attn = {o:0, t:0}, quiz = {o:0, t:0}, othersO = 0, othersM = 0;
     
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length < 4) return;
                const name = cells[1].innerText.trim().toLowerCase();
                const total = parseMark(cells[2].innerText);
                const obtained = parseMark(cells[3].innerText);
     
                if (isTheory) {
                    if (name.includes('class test')) cts.push({o: obtained, t: total});
                    else if (name.includes('mid term')) mid = {o: obtained, t: total};
                    else if (name.includes('project') || name.includes('assignment')) assign = {o: obtained, t: total};
                    else if (name.includes('attendance')) attn = {o: obtained, t: total};
                } else {
                    if (name.includes('quiz')) {
                        quiz.o += obtained;
                        quiz.t += total;
                    } else {
                        othersO += obtained;
                        othersM += total;
                    }
                }
            });
     
            let totalObtained = 0, maxMarks = 0;
     
            if (isTheory) {
                cts.sort((a, b) => b.o - a.o);
                let ctScore = 0;
                const top3 = cts.slice(0, 3);
                if (top3.length > 0) {
                    let sO = top3.reduce((a,b)=>a+b.o,0), sT = top3.reduce((a,b)=>a+b.t,0);
                    if(sT>0) ctScore = (sO/sT)*10;
                }
                let midScore = (mid.t>0)?(mid.o/mid.t)*20:0;
                let assScore = (assign.t>0)?(assign.o/assign.t)*10:0;
                let attScore = (attn.t>0)?(attn.o/attn.t)*10:0;
                totalObtained = ctScore + midScore + assScore + attScore;
                maxMarks = 50.00;
            } else {
                let quizScore = (quiz.t>0) ? (quiz.o/quiz.t)*20 : 0;
                let quizMax = (quiz.t>0) ? 20 : 0;
                totalObtained = quizScore + othersO;
                maxMarks = quizMax + othersM;
            }
     
            const resultRow = table.querySelector('#' + RESULT_ROW_ID);
            if (resultRow) {
                resultRow.cells[2].innerText = maxMarks.toFixed(2);
                resultRow.cells[3].innerText = totalObtained.toFixed(2);
            } else {
                createResultRow(table, totalObtained, maxMarks);
            }
     
            renderGradePredictor(table, totalObtained, isTheory);
        }
     
        // --- 3. Editable Cells Logic (With Validation) ---
        function makeCellsEditable(table) {
            const rows = Array.from(table.querySelectorAll('tbody tr')).filter(tr => !tr.querySelector('th') && tr.id !== RESULT_ROW_ID);
     
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length < 4) return;
                const targetCell = cells[3];
                const maxCell = cells[2];
     
                if (targetCell.getAttribute('data-processed') === 'true') return;
                targetCell.setAttribute('data-processed', 'true');
     
                const currentText = targetCell.innerText.trim();
                if (currentText !== '--') return;
     
                targetCell.style.cursor = 'pointer';
                targetCell.title = "Mark Missing: Click to Simulate";
                targetCell.style.backgroundColor = '#fff3cd';
                targetCell.style.border = '1px dashed #ffc107';
     
                targetCell.onclick = function() {
                    if (this.querySelector('input')) return;
     
                    const val = (this.innerText.trim() === '--') ? '' : this.innerText.trim();
                    const maxVal = parseFloat(maxCell.innerText.trim()) || 100;
     
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.value = val;
                    input.style.width = '60px';
                    input.style.padding = '2px';
                    input.style.textAlign = 'center';
     
                    const save = () => {
                        let newVal = parseFloat(input.value);
     
                        if (isNaN(newVal)) {
                            this.innerText = '--';
                        } else {
                            if (newVal < 0) newVal = 0;
                            if (newVal > maxVal) newVal = maxVal;
     
                            this.innerText = newVal.toFixed(2);
                        }
     
                        updateCalculations(table);
                    };
     
                    input.onblur = save;
                    input.onkeydown = (e) => { if(e.key === 'Enter') save(); };
     
                    this.innerText = '';
                    this.appendChild(input);
                    input.focus();
                };
            });
        }
     
        // --- 4. Init Row ---
        function createResultRow(table, totalObtained, maxMarks) {
            if (table.querySelector('#' + RESULT_ROW_ID)) return;
            const tr = document.createElement('tr');
            tr.id = RESULT_ROW_ID;
            tr.style.backgroundColor = '#d1e7dd';
            tr.style.fontWeight = 'bold';
            tr.style.color = '#0f5132';
            tr.style.borderTop = '2px solid #0f5132';
     
            tr.innerHTML = `<td></td><td align="right" style="padding-right:15px;">Total Obtained</td>
                            <td align="center">${maxMarks.toFixed(2)}</td><td align="center">${totalObtained.toFixed(2)}</td>`;
     
            table.querySelector('tbody').appendChild(tr);
        }
     
        // --- Main Engine ---
        setInterval(() => {
            const table = document.querySelector(`table[id$="${TABLE_ID_PARTIAL}"]`);
     
            if (table) {
                makeCellsEditable(table);
                if (!table.querySelector('#' + RESULT_ROW_ID)) {
                    updateCalculations(table);
                }
            }
        }, 1000);
     
    })();

