<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";
    import { ReportType } from "@/types/types";

    const analysisStore = useAnalysisOptions();

    function handleReportTypeChange(payload: string | number) {
        const value = payload.toString();

        if (value !== ReportType.SABER11 && value !== ReportType.SABERPRO)
            return;

        analysisStore.setReportType(value);
        analysisStore.clear("period");
        analysisStore.clear("institution");
    }
</script>

<template>
    <div>
        <span class="font-semibold">Report Type</span>
        <Select
            :default-value="ReportType.SABER11"
            @update:model-value="handleReportTypeChange"
        >
            <SelectTrigger class="mt-2">
                <SelectValue placeholder="Select the Report Type" />
            </SelectTrigger>
            <SelectContent>
                <SelectItem
                    v-for="type in ReportType"
                    :key="type"
                    :value="type"
                >
                    {{ type }}
                </SelectItem>
            </SelectContent>
        </Select>
    </div>
</template>
