
import re
import sys

def convert_line(line, current_address):
    # Remove comments/whitespace for processing but keep logic clean
    parts = line.split()
    if not parts:
        return line, current_address

    # Handle Set Address: 980EF100 00000000 ADDR
    # Example: 980EF100 00000000 003020E8
    if parts[0] == "980EF100" and len(parts) >= 3:
        current_address = int(parts[2], 16)
        # return None, current_address # Don't output address setting lines directly? 
        # Actually user example shows them replaced by the writes. 
        # But wait, looking at user example:
        # Original:
        # [One Hit Kill(while pressing ZL)]
        # 980EF100 00000000 003020E8 
        # 640E1000 00000000 946FC7B5 
        # ...
        # Converted:
        # [One Hit Kill(while pressing ZL)]
        # 04010000 003020E8 946FC7B5 
        
        # so the 980 line produces NOTHING in output, it just sets state.
        return None, current_address

    # Handle 640E1000 WORD2 WORD3
    # Example: 640E1000 00000000 946FC7B5
    if parts[0] == "640E1000" and len(parts) >= 3:
        word2 = parts[1]
        word3 = parts[2]
        
        # Check address region
        # If Main NSO (starts with 00xxxxxx) -> Type 04 (32-bit write)
        if current_address < 0x01000000: # Simple heuristic for 00... vs 01...
            # Output: 04010000 ADDR WORD3
            new_line = f"04010000 {current_address:08X} {word3}"
            return new_line, current_address
        else:
            # If Heap (starts with 01xxxxxx) -> Type 08 (64-bit write)
            # Output: 08010000 ADDR WORD2 WORD3
            new_line = f"08010000 {current_address:08X} {word2} {word3}"
            return new_line, current_address

    # Handle 680E1000 WORD2 WORD3 (Block Write / Burst)
    # Example: 680E1000 180000E7 4B080128
    if parts[0] == "680E1000" and len(parts) >= 3:
        val_at_addr_plus_4 = parts[1] # WORD2 goes to ADDR + 4 (based on user example 180000E7 is at C0)
        val_at_addr = parts[2]        # WORD3 goes to ADDR     (based on user example 4B080128 is at BC)
        
        # Note: User example:
        # 04010000 01EF3FBC 4B080128  <-- WORD3 (parts[2])
        # 04010000 01EF3FC0 180000E7  <-- WORD2 (parts[1])
        
        line1 = f"04010000 {current_address:08X} {val_at_addr}"
        line2 = f"04010000 {current_address + 4:08X} {val_at_addr_plus_4}"
        
        current_address += 8
        return f"{line1}\n{line2}", current_address

    # Pass through other lines (comments, existing codes, terminators)
    return line.strip(), current_address

def process_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    output_lines = []
    current_address = 0

    for line in lines:
        line = line.strip()
        if not line:
            output_lines.append("")
            continue
            
        if line.startswith('[') and line.endswith(']'):
            output_lines.append(line)
            continue
            
        result, current_address = convert_line(line, current_address)
        if result is not None:
            output_lines.append(result)

    return "\n".join(output_lines)

if __name__ == "__main__":
    input_file = r"C:\Users\zxa2\.gemini\antigravity\scratch\7F59549F6E792936.txt"
    try:
        new_content = process_file(input_file)
        # Write back to file or print? Let's write back for the user.
        with open(input_file, 'w') as f:
            f.write(new_content)
        print("Conversion successful.")
    except Exception as e:
        print(f"Error: {e}")
