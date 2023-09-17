test "{{ test_name }}" {
    // {{ character_literal_as_u8 }}
    const string = [_]u8{ 'a', 'b', 'c' };

    for (string, 0..) |character, index| {
        _ = character; // {{ current_array_elem }}
        _ = index; // {{ current_index }}
    }

    for (string) |character| {
        _ = character;
    }

    for (string, 0..) |_, index| {
        _ = index;
    }

    for (string) |_| {}
}
