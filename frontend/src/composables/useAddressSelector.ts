import { ref, computed, watch } from 'vue'
import { taiwanAddressData } from '@/mock/data/taiwan-address'
import type { CountyData, DistrictData } from '@/mock/data/taiwan-address'

export function useAddressSelector() {
  const selectedCounty = ref('')
  const selectedDistrict = ref('')
  const selectedVillage = ref('')
  const addressDetail = ref('')

  const counties = computed(() =>
    taiwanAddressData.map((c) => ({ code: c.code, name: c.name })),
  )

  const currentCountyData = computed<CountyData | undefined>(() =>
    taiwanAddressData.find((c) => c.code === selectedCounty.value),
  )

  const districts = computed(() =>
    currentCountyData.value?.districts.map((d) => ({ code: d.code, name: d.name })) || [],
  )

  const currentDistrictData = computed<DistrictData | undefined>(() =>
    currentCountyData.value?.districts.find((d) => d.code === selectedDistrict.value),
  )

  const villages = computed(() =>
    currentDistrictData.value?.villages || [],
  )

  // 當縣市變更時清除區和里
  watch(selectedCounty, () => {
    selectedDistrict.value = ''
    selectedVillage.value = ''
  })

  // 當區變更時清除里
  watch(selectedDistrict, () => {
    selectedVillage.value = ''
  })

  function setAddress(countyCode: string, districtCode: string, villageCode: string, detail: string) {
    selectedCounty.value = countyCode
    // 需要等 watch 生效後再設定
    setTimeout(() => {
      selectedDistrict.value = districtCode
      setTimeout(() => {
        selectedVillage.value = villageCode
        addressDetail.value = detail
      }, 0)
    }, 0)
  }

  function getFullAddress() {
    const county = currentCountyData.value?.name || ''
    const district = currentDistrictData.value?.name || ''
    const village = selectedVillage.value || ''
    return `${county}${district}${village}${addressDetail.value}`
  }

  return {
    selectedCounty,
    selectedDistrict,
    selectedVillage,
    addressDetail,
    counties,
    districts,
    villages,
    setAddress,
    getFullAddress,
  }
}
