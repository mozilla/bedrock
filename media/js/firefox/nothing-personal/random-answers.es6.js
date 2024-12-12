/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let randomizerButton;
let randomOutput;
let answers;
let mutableAnswers;

function getRandomAnswer(answers) {
    // set a mutable array we can work through, reset it when empty
    if (mutableAnswers === undefined || mutableAnswers.length === 0) {
        mutableAnswers = [...answers];
    }
    const answerIndex = Math.floor(Math.random() * mutableAnswers.length);
    // mutate array to remove answer so we can't repeat it, return answer
    return mutableAnswers.splice(answerIndex, 1);
}

function setRandomAnswer(container, answers) {
    container.textContent = getRandomAnswer(answers);
}

function init() {
    randomizerButton = document.getElementById('randomizer-button');
    randomOutput = document.getElementById('random-output');

    answers = Array.from(document.querySelectorAll('#things-list li')).map(
        (li) => li.textContent
    );

    // set new answer on button click
    randomizerButton.addEventListener('click', () => {
        setRandomAnswer(randomOutput, answers);
    });

    // set initial random answer on load
    setRandomAnswer(randomOutput, answers);
}

init();
