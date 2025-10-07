<template>
  <form class="grid-auto" @submit.prevent="handleSubmit">
    <div class="grid-2">
      <div class="field">
        <label>Отдаю</label>
        <div class="input crypto-select">
          <img :src="coinLogo" alt="coin" class="coin-logo" />
          <select :value="crypto" @change="onCryptoChange($event.target.value)">
            <option value="USDT">USDT</option>
            <option value="BTC">BTC</option>
            <option value="ETH">ETH</option>
            <option value="TON">TON</option>
          </select>
          <input v-model.number="cryptoAmount" type="number" min="0" step="0.0001" placeholder="Сумма" />
          <span class="suffix">{{ crypto }}</span>
        </div>
      </div>
      <div class="field">
        <label>Получаю (RUB)</label>
        <div class="input" style="cursor: not-allowed">
          <input :value="rubAmountDisplay" inputmode="numeric" readonly />
          <span class="suffix">RUB</span>
        </div>
      </div>
    </div>

    <div class="grid-2">
      <div class="field">
        <label>Банк получателя</label>
        <div class="input bank-select">
          <img :src="bankLogo" alt="logo" class="bank-logo" />
          <select v-model="bank">
            <option value="sber">Сбер</option>
            <option value="tinkoff">Тбанк</option>
            <option value="vtb">ВТБ</option>
            <option value="alfa">Альфа банк</option>
            <option value="raif">Райффайзен банк</option>
            <option value="gazprom">Газпромбанк</option>
            <option value="rosselhoz">Россельхоз</option>
            <option value="rosbank">Росбанк</option>
            <option value="otkritie">Открытие</option>
            <option value="pochtabank">Почта Банк</option>
            <option value="uralsib">Уралсиб</option>
            <option value="sovcom">Совкомбанк</option>
            <option value="ozon">Озон банк</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label>Карта получателя</label>
        <div class="input">
          <input v-model="card" placeholder="0000 0000 0000 0000" maxlength="19" @input="formatCard" />
        </div>
      </div>
    </div>

    <div class="grid-2">
      <div class="field">
        <label>Имя держателя карты</label>
        <div class="input">
          <input v-model="holder" placeholder="IVAN IVANOV" @input="toUpper" />
        </div>
      </div>
      <div class="field">
        <label>Контакт (Telegram)</label>
        <div class="input">
          <input v-model="telegram" placeholder="@username" />
        </div>
      </div>
    </div>

    <div class="rate-box" style="cursor: not-allowed">
      <span>Курс конвертации</span>
      <strong>1 {{ crypto }} ≈ {{ rate.toLocaleString('ru-RU') }} RUB</strong>
    </div>

    <p :style="{margin: '4px 2px 0', fontSize: '12px', color: meetsMinRub ? '#93a4b0' : '#fda4af'}">
      {{ meetsMinRub ? 'Минимальный вывод — 225 RUB' : 'Минимальная сумма к получению — 225 RUB' }}
    </p>

    <p :style="{margin: '4px 2px 0', fontSize: '12px', color: meetsMinRub ? '#93a4b0' : '#fda4af'}">
      {{ rubAmount < 1000 ? 'Маленькие суммы требуют больше времени на вывод (до 1 часа)' : '' }}
    </p>

    <button class="submit-btn" type="submit" :disabled="!canSubmit">Создать заявку</button>
  </form>
  
  <p v-if="error" style="color: #fda4af; margin: 8px 2px 0; font-size: 12px;">{{ error }}</p>
</template>

<script setup>
import { computed, reactive, toRefs, watch } from 'vue';

const props = defineProps({
  rate: { type: Number, required: true },
  crypto: { type: String, required: true }
});
const emit = defineEmits(['submit-order', 'update:crypto']);

const state = reactive({
  cryptoAmount: 100,
  bank: 'tinkoff',
  card: '',
  holder: '',
  telegram: '',
  error: ''
});

const { cryptoAmount, bank, card, holder, telegram, error } = toRefs(state);
const crypto = computed(() => props.crypto);

const rate = computed(() => props.rate);
const rubAmount = computed(() => Math.max(0, Number(cryptoAmount.value || 0)) * rate.value);
const MIN_RUB = 225;
const meetsMinRub = computed(() => rubAmount.value >= MIN_RUB);
const rubAmountDisplay = computed(() => rubAmount.value.toLocaleString('ru-RU'));

const canSubmit = computed(() => {
  return (
    Number(cryptoAmount.value) > 0 &&
    meetsMinRub.value &&
    validateCard(card.value) &&
    holder.value.trim().length >= 3 &&
    validateTelegram(telegram.value)
  );
});

watch(cryptoAmount, () => { state.error = ''; });

function formatCard(e) {
  const digits = e.target.value.replace(/\D/g, '').slice(0, 16);
  const groups = digits.match(/\d{1,4}/g) || [];
  state.card = groups.join(' ');
}

function toUpper() { state.holder = state.holder.toUpperCase(); }

function validateCard(num) { return /^\d{4} \d{4} \d{4} \d{4}$/.test(num); }
function validateTelegram(u) { return /^@?[a-zA-Z0-9_]{5,}$/.test(u.trim()); }

function handleSubmit() {
  if (!canSubmit.value) {
    state.error = !meetsMinRub.value
      ? 'Минимальная сумма к получению — 225 RUB'
      : 'Проверьте корректность данных формы';
    return;
  }
  state.error = '';
  emit('submit-order', {
    crypto: crypto.value,
    cryptoAmount: Number(state.cryptoAmount),
    rubAmount: rubAmount.value,
    bank: state.bank,
    card: state.card,
    holder: state.holder,
    telegram: state.telegram
  });
}

function onCryptoChange(val) {
  emit('update:crypto', val);
}

const bankLogo = computed(() => {
  const map = {
    sber: '/banks/icon_sber-01.png',
    tinkoff: '/banks/tbank.png',
    vtb: '/banks/vtb.svg',
    alfa: '/banks/1408.svg',
    ozon: '/banks/ozon.png',
    raif: '/banks/raif.png'
  };
  return map[bank.value] || '/banks/also.png';
});

const coinLogo = computed(() => {
  const map = {
    USDT: '/coins/tether.svg',
    BTC: '/coins/Bitcoin.svg.png',
    ETH: '/coins/ethereum-eth.svg',
    TON: '/coins/ton_symbol.png'
  };
  return map[crypto.value] || '/coins/usdt.svg';
});
</script>

<style scoped>
/* component-specific tweaks if needed */
.bank-select { gap: 8px; }
.bank-logo { width: 20px; height: 20px; border-radius: 5px; }
.crypto-select { gap: 8px; }
.coin-logo { width: 20px; height: 20px; border-radius: 50%; }
</style>


