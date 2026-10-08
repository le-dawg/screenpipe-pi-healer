function modelFromJson(providerId, definition, providerConfig, defaults) {
    const api = definition.api ?? providerConfig.api ?? defaults?.api;
    if (!api) {
        throw new Error(`Provider ${providerId}, model ${definition.id}: no "api" specified. Set at provider or model level.`);
    }
    return {
        id: definition.id,
        name: definition.name ?? definition.id,
        api: api,
        provider: providerId,
        baseUrl,
        reasoning: definition.reasoning ?? false,
    };
}
