use std::collections::HashMap;

pub fn calc_frequency(text: impl Iterator<Item = char> + Clone) -> HashMap<char, f32> {
    let mut map = HashMap::new();
    for char in text {
        *map.entry(char).or_insert(0f32) += 1f32;
    }
    map
}

pub fn calc_coincidence(text: impl Iterator<Item = char> + Clone) -> f32 {
    let text_len = text.clone().count() as f32;
    let map = calc_frequency(text);
    let mut coincidence: f32 = map.values().fold(0f32, |result, frequency| {
        result + frequency * (frequency - 1f32)
    });
    coincidence *= 1f32 / (text_len * (text_len - 1f32));
    coincidence
}
