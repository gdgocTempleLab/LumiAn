<script setup lang="ts">
import { useAddressSelector } from '@/composables/useAddressSelector'
import { watch } from 'vue'

const props = defineProps<{
  modelValue?: {
    countyCode: string
    districtCode: string
    villageName: string
    detail: string
  }
}>()

const emit = defineEmits<{
  'update:modelValue': [value: {
    countyCode: string
    countyName: string
    districtCode: string
    districtName: string
    villageName: string
    detail: string
  }]
}>()

const {
  selectedCounty,
  selectedDistrict,
  selectedVillage,
  addressDetail,
  counties,
  districts,
  villages,
} = useAddressSelector()

// 初始化
if (props.modelValue) {
  selectedCounty.value = props.modelValue.countyCode
  selectedDistrict.value = props.modelValue.districtCode
  selectedVillage.value = props.modelValue.villageName
  addressDetail.value = props.modelValue.detail
}

function emitUpdate() {
  const county = counties.value.find((c) => c.code === selectedCounty.value)
  const district = districts.value.find((d) => d.code === selectedDistrict.value)
  emit('update:modelValue', {
    countyCode: selectedCounty.value,
    countyName: county?.name || '',
    districtCode: selectedDistrict.value,
    districtName: district?.name || '',
    villageName: selectedVillage.value,
    detail: addressDetail.value,
  })
}

watch([selectedCounty, selectedDistrict, selectedVillage, addressDetail], emitUpdate)
</script>

<template>
  <div class="address-cascader">
    <div class="address-selects">
      <el-select v-model="selectedCounty" placeholder="縣市" class="addr-select">
        <el-option
          v-for="c in counties"
          :key="c.code"
          :label="`${c.code}${c.name}`"
          :value="c.code"
        />
      </el-select>

      <el-select v-model="selectedDistrict" placeholder="鄉鎮市區" class="addr-select">
        <el-option
          v-for="d in districts"
          :key="d.code"
          :label="d.name"
          :value="d.code"
        />
      </el-select>

      <el-select v-model="selectedVillage" placeholder="村里" class="addr-select">
        <el-option
          v-for="v in villages"
          :key="v"
          :label="v"
          :value="v"
        />
      </el-select>
    </div>

    <el-input
      v-model="addressDetail"
      placeholder="詳細地址"
      class="address-detail"
    />
  </div>
</template>

<style scoped lang="scss">
.address-cascader {
  max-width: 420px;
}

.address-selects {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.addr-select {
  flex: 1;
  min-width: 0;
}

.address-detail {
  width: 100%;
}
</style>
