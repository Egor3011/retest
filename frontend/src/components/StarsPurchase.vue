<template>
  <form class="grid-auto" @submit.prevent="submit">
    <div class="grid-2">
      <div class="field">
        <label>Пакет звёзд</label>
        <div class="input">
          <select v-model.number="stars">
            <option :value="50">50 ⭐</option>
            <option :value="100">100 ⭐</option>
            <option :value="250">250 ⭐</option>
            <option :value="500">500 ⭐</option>
            <option :value="1000">1000 ⭐</option>
            <option :value="2500">2500 ⭐</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label>Оплата криптовалютой</label>
        <div class="input crypto-select">
          <img :src="coinLogo" alt="coin" class="coin-logo" />
          <select v-model="crypto">
            <option value="TON">TON</option>
            <option value="TOH">TOH</option>
          </select>
          <span class="suffix">{{ crypto }}</span>
        </div>
      </div>
    </div>

    <div class="grid-2">
      <div class="field">
        <label>Цена в RUB ( 1 ⭐ = {{ rub / stars }} RUB ) </label>
        <div class="input" style="cursor:not-allowed">
          <input :value="rubDisplay" readonly />
          <span class="suffix">RUB</span>
        </div>
      </div>
      <div class="field">
        <label>Отправить ({{ crypto }})</label>
        <div class="input" style="cursor:not-allowed">
          <input :value="cryptoAmountDisplay" readonly />
          <span class="suffix">{{ crypto }}</span>
        </div>
      </div>
    </div>

    <div class="field">
      <label>Ваш Telegram @username</label>
      <div class="input">
        <input v-model="telegram" placeholder="@username" />
      </div>
    </div>

    <div class="rate-box">
      <span>Курс: 1 {{ crypto }} ≈ {{ rate.toLocaleString('ru-RU') }} ₽</span>
      <strong>{{ stars }} ⭐</strong>
    </div>

    <button class="submit-btn" type="submit" :disabled="!canSubmit">Купить ⭐</button>
  </form>
</template>

<script setup>
import { computed, reactive, toRefs } from 'vue';

const props = defineProps({ rate: { type: Number, required: true } });
const emit = defineEmits(['submit-stars']);

const state = reactive({
  stars: 250,
  crypto: 'TON',
  telegram: ''
});

const { stars, crypto, telegram } = toRefs(state);
const rate = computed(() => props.rate);

const rub = computed(() => Math.ceil(stars.value * 1.13)); // пример: 1⭐ ≈ 1.2 RUB
const cryptoAmount = computed(() => Number((rub.value / rate.value).toFixed(6)));
const rubDisplay = computed(() => rub.value.toLocaleString('ru-RU'));
const cryptoAmountDisplay = computed(() => cryptoAmount.value.toString());

const canSubmit = computed(() => /^@?[a-zA-Z0-9_]{5,}$/.test(telegram.value.trim()));

function submit() {
  if (!canSubmit.value) return;
  emit('submit-stars', {
    stars: stars.value,
    crypto: crypto.value,
    cryptoAmount: cryptoAmount.value,
    rub: rub.value,
    telegram: telegram.value
  });
}

const coinLogo = computed(() => {
  const map = { TON: '/coins/ton_symbol.png', TOH: '/coins/ton_symbol.png' }; // TOH uses TON icon
  return map[crypto.value] || '/coins/ton_symbol.png';
});
</script>

<style scoped>
.crypto-select { gap: 8px; }
.coin-logo { width: 20px; height: 20px; border-radius: 50%; }
</style>


