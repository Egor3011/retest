<template>
  <teleport to="body">
    <div v-if="visible" class="overlay" @click.self="onClose">
      <div class="modal panel">
        <header class="modal-header">
          <h3>Перевод {{ order?.crypto }} → RUB</h3>
          <button class="icon-btn" @click="onClose" aria-label="Закрыть">✕</button>
        </header>

        <div class="modal-body">
          <div class="hint">Отправьте точно указанную сумму на кошелёк ниже. После отправки нажмите «Я перевёл».</div>

          <div class="grid-auto" style="gap:10px">
            <div class="info-row">
              <span>Сумма к переводу</span>
              <strong>{{ amountDisplay }}</strong>
            </div>
            <div class="info-row">
              <span>Сеть</span>
              <strong>{{ networkLabel }}</strong>
            </div>
          </div>

          <div class="wallet-box">
            <label>Адрес для перевода</label>
            <div class="wallet-input">
              <input :value="address" readonly />
              <button class="copy-btn" @click="copy">Копировать</button>
            </div>
          </div>

          <div v-if="qr" class="qr-box">
            <img :src="qr" alt="QR" />
          </div>

          <p v-if="copied" class="copied">Адрес скопирован</p>
        </div>

        <footer class="modal-footer">
          <button class="secondary" @click="onClose">Отмена</button>
          <button class="primary" @click="confirm">Я перевёл</button>
        </footer>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  visible: { type: Boolean, default: false },
  order: { type: Object, default: null },
  address: { type: String, required: true },
  network: { type: String, default: '' },
  qr: { type: String, default: '' }
});
const emit = defineEmits(['close', 'confirm']);

const copied = ref(false);

const amountDisplay = computed(() => {
  if (!props.order) return '';
  const val = Number(props.order.cryptoAmount || 0);
  return `${val} ${props.order.crypto}`;
});

const networkLabel = computed(() => props.network || '—');

async function copy() {
  try {
    await navigator.clipboard.writeText(props.address);
    copied.value = true;
    setTimeout(() => (copied.value = false), 1500);
  } catch {}
}

function onClose() { emit('close'); }
function confirm() { emit('confirm'); }
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0; display: grid; place-items: center;
  background: rgba(0,0,0,0.6);
  z-index: 50;
}
.modal {
  width: min(560px, calc(100vw - 24px));
  border-radius: var(--radius-xl);
}
.modal-header { display:flex; justify-content:space-between; align-items:center; padding: 14px 16px; border-bottom: 1px solid rgba(255,255,255,0.06); }
.modal-body { padding: 14px 16px; display:grid; gap: 12px; }
.modal-footer { padding: 14px 16px; display:flex; justify-content:flex-end; gap: 8px; border-top: 1px solid rgba(255,255,255,0.06); }
.icon-btn { background: transparent; border: none; color: var(--tg-text); font-size: 18px; cursor: pointer; }
.hint { color: var(--tg-muted); font-size: 13px; }
.info-row { display:flex; justify-content:space-between; color: var(--tg-muted); font-size: 13px; }
.info-row strong { color: var(--tg-text); }
.wallet-box label { color: var(--tg-muted); font-size: 12px; }
.wallet-input { display:flex; gap: 8px; align-items:center; }
.wallet-input input { flex:1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); color: var(--tg-text); border-radius: var(--radius-lg); padding: 10px 12px; }
.copy-btn { background: rgba(34,158,217,0.12); border: 1px solid rgba(34,158,217,0.25); color: #bfe9ff; border-radius: 12px; padding: 10px 12px; cursor: pointer; }
.copied { color: #86efac; font-size: 12px; margin: 0; }
.qr-box { display:grid; place-items:center; padding-top: 8px; }
.qr-box img { width: 160px; height: 160px; border-radius: 10px; background: white; }
.secondary { background: transparent; border: 1px solid rgba(255,255,255,0.12); color: var(--tg-text); padding: 10px 14px; border-radius: var(--radius-lg); cursor:pointer; }
.primary { background: linear-gradient(135deg, var(--tg-accent-2), var(--tg-accent)); border: none; color: white; padding: 10px 14px; border-radius: var(--radius-lg); cursor:pointer; box-shadow: 0 10px 24px rgba(34,158,217,0.35); }
</style>


