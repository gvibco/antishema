const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const scenarios = require('../js/scenarios.js');
const { validateScenarios } = require('../js/engine.js');

test('в наборе десять сценариев', () => {
  assert.ok(Array.isArray(scenarios));
  assert.equal(scenarios.length, 10);
});

test('присутствуют оба типа заданий', () => {
  const types = new Set(scenarios.map((scenario) => scenario.type));
  assert.ok(types.has('dialog'));
  assert.ok(types.has('recognize'));
});

test('все сценарии проходят валидацию', () => {
  assert.deepEqual(validateScenarios(scenarios), []);
});

test('у каждого сценария есть красный флаг', () => {
  for (const scenario of scenarios) {
    assert.ok(scenario.redFlag, `Нет красного флага: ${scenario.id}`);
  }
});

test('правильные ответы не стоят всегда на одном месте', () => {
  const positions = new Set(
    scenarios.map((scenario) => scenario.choices.findIndex((choice) => choice.correct)),
  );
  assert.ok(positions.size > 1);
});

test('в распознавании есть и безопасное, и мошенническое сообщение', () => {
  const recognition = scenarios.filter((scenario) => scenario.type === 'recognize');
  const correctLabels = recognition.map(
    (scenario) => scenario.choices.find((choice) => choice.correct).text,
  );
  assert.ok(correctLabels.some((label) => label === 'Безопасно'));
  assert.ok(correctLabels.some((label) => label === 'Похоже на мошенничество'));
});

test('страница правил содержит 12 правил', () => {
  const html = fs.readFileSync(path.join(__dirname, '..', 'rules.html'), 'utf8');
  assert.equal((html.match(/class="rule-card"/g) || []).length, 12);
  assert.ok(html.includes('Если уже обманули'));
});
