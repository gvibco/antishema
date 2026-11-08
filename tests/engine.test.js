const test = require('node:test');
const assert = require('node:assert/strict');
const {
  createGame,
  submitAnswer,
  getResult,
  validateScenarios,
} = require('../js/engine.js');

function scenario(id, correctId = 'ok') {
  return {
    id,
    type: 'dialog',
    title: `Сценарий ${id}`,
    messages: [{ from: 'them', text: 'Проверочное сообщение' }],
    choices: [
      { id: correctId, text: 'Верно', correct: true },
      { id: 'bad', text: 'Неверно', correct: false },
    ],
    explanation: 'Объяснение',
    redFlag: 'Красный флаг',
    rule: 'Правило',
  };
}

const scenarios = [scenario('a'), scenario('b'), scenario('c'), scenario('d'), scenario('e')];

test('новая игра начинается с нуля', () => {
  const game = createGame(scenarios);
  assert.equal(game.index, 0);
  assert.equal(game.score, 0);
  assert.equal(game.finished, false);
});

test('верный ответ увеличивает счёт', () => {
  const result = submitAnswer(createGame(scenarios), scenarios, 'ok');
  assert.equal(result.correct, true);
  assert.equal(result.game.score, 1);
  assert.equal(result.game.index, 1);
});

test('неверный ответ не увеличивает счёт', () => {
  const result = submitAnswer(createGame(scenarios), scenarios, 'bad');
  assert.equal(result.correct, false);
  assert.equal(result.game.score, 0);
  assert.equal(result.game.index, 1);
});

test('ответ на последний сценарий завершает игру', () => {
  const short = [scenario('a'), scenario('b'), scenario('c')];
  let game = createGame(short);
  game = submitAnswer(game, short, 'ok').game;
  game = submitAnswer(game, short, 'ok').game;
  game = submitAnswer(game, short, 'ok').game;
  assert.equal(game.finished, true);
  assert.equal(game.score, 3);
  assert.equal(game.answers.length, 3);
});

test('нельзя отвечать после завершения игры', () => {
  let game = createGame([scenario('a')]);
  game = submitAnswer(game, [scenario('a')], 'ok').game;
  assert.equal(submitAnswer(game, [scenario('a')], 'ok'), null);
});

test('результат считает процент и уровень', () => {
  const result = getResult({ score: 3, total: 3 }, scenarios);
  assert.equal(result.percent, 100);
  assert.equal(result.level, 'expert');
});

test('уровни результата различаются на границах', () => {
  assert.equal(getResult({ score: 4, total: 6 }, scenarios).level, 'confident');
  assert.equal(getResult({ score: 3, total: 6 }, scenarios).level, 'learner');
  assert.equal(getResult({ score: 2, total: 6 }, scenarios).level, 'risk');
});

test('валидация пропускает корректные сценарии', () => {
  assert.deepEqual(validateScenarios(scenarios), []);
});

test('валидация ловит сценарий без правильного ответа', () => {
  const broken = scenario('broken');
  broken.choices = broken.choices.map((choice) => ({ ...choice, correct: false }));
  const errors = validateScenarios([...scenarios, broken]);
  assert.ok(errors.some((error) => error.includes('правильный ответ')));
});

test('валидация ловит отсутствие красного флага', () => {
  const broken = { ...scenario('broken') };
  delete broken.redFlag;
  const errors = validateScenarios([...scenarios, broken]);
  assert.ok(errors.some((error) => error.includes('красный флаг')));
});

test('валидация ловит неизвестный тип задания', () => {
  const broken = { ...scenario('broken'), type: 'unknown' };
  const errors = validateScenarios([...scenarios, broken]);
  assert.ok(errors.some((error) => error.includes('тип')));
});
