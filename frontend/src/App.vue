<template>
  <div class="wrap">
    <header class="app-header">
      <div class="container brand">
        <div class="brand-badge" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="24" height="24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8Zm-1-13h2v6l4.5 2.7-1 1.6L11 13V7Z" fill="#fff"/></svg>
        </div>
        <div>
          <div class="brand-title">FastX • Обменник</div>
          <div class="brand-sub">Моментальный обмен криптовалюты на карту</div>
        </div>
      </div>
    </header>

    <main class="container hero">
      <section class="panel exchange-card">
        <div class="exchange-header">
          <h2 style="margin:0">{{ mode === 'exchange' ? 'Обмен криптовалюты → RUB' : 'Покупка Telegram ⭐' }}</h2>
          <span class="pill">~10-15 мин</span>
        </div>

        <div class="mode-switch">
          <button
            :class="['mode-btn', mode==='exchange' ? 'active' : '']"
            @click="mode='exchange'"
            type="button"
          >RUB</button>
          <button
            :class="['mode-btn', mode==='stars' ? 'active' : '']"
            @click="mode='stars'"
            type="button"
          >⭐ Звёзды</button>
        </div>

        <ExchangeForm v-if="mode==='exchange'"
          @submit-order="onSubmitOrder"
          :rate="rate"
          :crypto="selectedCrypto"
          @update:crypto="selectedCrypto = $event"
        />

        <StarsPurchase v-else
          :rate="starsRate"
          @submit-stars="onSubmitStars"
        />

        <PaymentModal
          :visible="isModalOpen"
          :order="lastOrder"
          :address="walletAddress"
          :network="walletNetwork"
          :qr="walletQr"
          @close="isModalOpen = false"
          @confirm="onConfirmTransfer"
        />
      </section>

      <aside class="panel aside">
        <h3>Почему мы</h3>
        <div class="list">
          <div class="item"><span>Быстро</span><strong>Обычно 10-15 минут</strong></div>
          <div class="item"><span>Комиссия</span><strong>Включена в курс</strong></div>
          <div class="item"><span>Поддержка</span><strong>24/7 в TG</strong></div>
          <div class="item"><span>Карта РФ</span><strong>Все основные банки</strong></div>
        </div>
      </aside>
    </main>

    <section class="panel cta">
      <div class="container cta-inner">
        <div class="cta-text">
          <h3 style="margin:0 0 6px">Нужна помощь с обменом?</h3>
          <p style="margin:0; color: var(--tg-muted);">Мы на связи в Telegram 24/7 и ответим за пару минут.</p>
        </div>
        <a class="cta-btn" href="https://t.me/fastx_support" target="_blank" rel="noopener">Открыть чат</a>
      </div>
    </section>

    <footer class="footer">
      © {{ year }} FastX — самый быстрый обменник криптовалюты в рубли.
    </footer>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick, onMounted } from 'vue';
import ExchangeForm from './components/ExchangeForm.vue';
import PaymentModal from './components/PaymentModal.vue';
import StarsPurchase from './components/StarsPurchase.vue';
import QRCode from 'qrcode';
import axios from "axios";

const year = new Date().getFullYear();

// Basic reactive rates per crypto (mock). In real app, fetch from backend.
const selectedCrypto = ref('USDT');
const mode = ref('exchange');
const baseRatesRub = ref({
  USDT: 81,   // RUB per 1 USDT
  BTC: 10395823,  // RUB per 1 BTC
  ETH: 387248,   // RUB per 1 ETH
  TON: 228,
  TOH: 228,     // RUB per 1 TON
});
const spread = ref(0.01); // 0.45% spread
const rate = computed(() => {
  const base = baseRatesRub.value[selectedCrypto.value] ?? baseRatesRub.value.USDT;
  return Math.round(base * (1 - spread.value));
});

onMounted(() => {
    axios.get("/api/new_user").then((res) => {
        console.log(res.data)
    })
})

const rateDisplay = computed(() => `1 ${selectedCrypto.value} ≈ ${rate.value.toLocaleString('ru-RU')} ₽`);


// Stars rate (always TON/TOH)
const starsRate = computed(() => {
  const base = baseRatesRub.value.TON; // Use TON rate for stars
  return Math.round(base * (1 - spread.value));
});

// Modal state
const isModalOpen = ref(false);
const lastOrder = ref(null);

// Wallets per crypto (mock demo). Replace with backend values.
const wallets = {
  USDT: { address: 'Врменно не доступно', network: 'TRC20', qr: '' },
  BTC: { address: 'Врменно не доступно', network: 'Bitcoin', qr: '' },
  ETH: { address: 'Врменно не доступно', network: 'Ethereum', qr: '' },
  TON: { address: 'UQBzbpV6m6fwk5sRQvsSfjJbfvMgtlKbXtixpJQ5usBIhHe-', network: 'TON', qr: '' },
  TOH: { address: 'UQBzbpV6m6fwk5sRQvsSfjJbfvMgtlKbXtixpJQ5usBIhHe-', network: 'TON', qr: '' }
};

const walletAddress = computed(() => wallets[selectedCrypto.value]?.address || '');
const walletNetwork = computed(() => wallets[selectedCrypto.value]?.network || '');
const walletQrData = ref('');
const walletQr = computed(() => walletQrData.value);

function onSubmitOrder(order) {
  lastOrder.value = order;
  isModalOpen.value = true;
}

function onConfirmTransfer() {
  isModalOpen.value = false;
  alert('Спасибо! Мы проверим перевод и свяжемся с вами.');
  console.log(walletAddress, walletNetwork, lastOrder.value)
  axios.post("/api/new_order", lastOrder.value).then(
    (res) => {
      alert('Спасибо! Мы проверим перевод и свяжемся с вами. Номер вашей заявки: ' + res.data.data);
    }
  )
}

function onSubmitStars(payload) {
  // Reuse wallet + modal
  selectedCrypto.value = payload.crypto;
  lastOrder.value = { crypto: payload.crypto, cryptoAmount: payload.cryptoAmount, rubAmount: payload.rub, bank: 'stars', card: '—', holder: payload.telegram, telegram: payload.telegram };
  isModalOpen.value = true;
}

// Generate QR when modal opens or dependencies change
async function generateQr() {
  const addr = walletAddress.value;
  if (!isModalOpen.value || !addr || /Вр?менно не доступно/i.test(addr)) {
    walletQrData.value = '';
    return;
  }
  // Build simple payload text; could be replaced with network-specific URIs
  const amount = lastOrder.value?.cryptoAmount;
  const asset = selectedCrypto.value;
  const text = `${asset}:${addr}${amount ? `?amount=${amount}` : ''}`;
  try {
    walletQrData.value = await QRCode.toDataURL(text, {
      errorCorrectionLevel: 'M',
      margin: 1,
      color: { dark: '#ffffff', light: '#00000000' }
    });
  } catch (e) {
    walletQrData.value = '';
  }
}

watch([isModalOpen, selectedCrypto, walletAddress, () => lastOrder.value?.cryptoAmount], async () => {
  await nextTick();
  generateQr();
});
</script>

<style scoped>
/* page-level tweaks only */
</style>


