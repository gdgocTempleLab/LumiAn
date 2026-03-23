<script setup lang="ts">
import { reactive, watch } from 'vue'
import AddressCascader from './AddressCascader.vue'

const props = defineProps<{
  modelValue: {
    phoneAreaCode: string
    phoneNumber: string
    mobile: string
    sameAsRegistered: boolean
    registeredAddress: {
      countyCode: string
      countyName: string
      districtCode: string
      districtName: string
      villageName: string
      detail: string
    }
    residenceAddress: {
      countyCode: string
      countyName: string
      districtCode: string
      districtName: string
      villageName: string
      detail: string
    }
  }
}>()

const emit = defineEmits<{
  'update:modelValue': [value: typeof props.modelValue]
}>()

const form = reactive({ ...props.modelValue })

watch(form, () => {
  emit('update:modelValue', { ...form })
}, { deep: true })

watch(() => props.modelValue, (val) => {
  Object.assign(form, val)
}, { deep: true })

watch(() => form.sameAsRegistered, (val) => {
  if (val) {
    form.residenceAddress = { ...form.registeredAddress }
  }
})
</script>

<template>
  <div class="household-form">
    <div class="form-row">
      <label class="form-label">電話（市話）：</label>
      <div class="phone-inputs">
        <el-input
          v-model="form.phoneAreaCode"
          placeholder="區碼"
          class="area-code-input"
        />
        <span class="separator">-</span>
        <el-input
          v-model="form.phoneNumber"
          placeholder="12345678"
          class="phone-number-input"
        />
      </div>
    </div>

    <div class="form-row">
      <label class="form-label">電話（手機）：</label>
      <el-input
        v-model="form.mobile"
        placeholder="09xxxxxxxx"
        class="mobile-input"
      />
    </div>

    <div class="form-row">
      <div class="address-header">
        <label class="form-label">
          居住地址：<span class="required-star">*</span>
        </label>
        <el-checkbox v-model="form.sameAsRegistered">同戶籍地址</el-checkbox>
      </div>
      <AddressCascader
        v-model="form.registeredAddress"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.household-form {
  padding: 24px 0;
}

.form-row {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  color: $temple-text-dark;
  margin-bottom: 8px;
}

.required-star {
  color: #f56c6c;
}

.phone-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.area-code-input {
  width: 60px;
}

.phone-number-input {
  width: 180px;
}

.separator {
  color: $temple-text-muted;
}

.mobile-input {
  width: 250px;
}

.address-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}
</style>
