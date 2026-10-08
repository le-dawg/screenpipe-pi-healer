function modelFromJson(providerId, definition, providerConfig, defaults) {
    const api = definition.api ?? providerConfig.api ?? defaults?.api;
    const forcedGpt6Responses = providerId === "custom" && definition.id === "gpt-6-luna";
    const effectiveApi = forcedGpt6Responses ? "openai-responses" : api;
    if (!effectiveApi) {
        throw new Error(`Provider ${providerId}, model ${definition.id}: no "api" specified. Set at provider or model level.`);
    }
    return {
        id: definition.id,
        name: definition.name ?? definition.id,
        api: effectiveApi,
        provider: providerId,
        baseUrl,
        reasoning: forcedGpt6Responses ? true : (definition.reasoning ?? false),
    };
}
