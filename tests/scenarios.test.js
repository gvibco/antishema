const test = require('node:test');
const assert = require('node:assert/strict');
const scenarios = require('../js/scenarios.js');
const { validateScenarios } = require('../js/engine.js');

test('в наборе не меньше пяти сценариев', () => {
  assert.ok(Array.isArray(scenarios));
  assert.ok(scenarios.length >= 5);
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
