from random import choice, choices, sample, randint
import shlex

HELP_MESSAGE = """NSR Bot được tạo bởi Nova(Tây tiền tỉ)
Cách gọi bot: Gọi NSR Bot bằng câu lệnh /nsr_bot
Cách sử dụng: /nsr_bot <động từ> <danh sách tham số>
Nếu có nhiều tham số thì tách nhau bằng dấu cách, nếu bản thân tham số đó có dấu phẩy thì đặt nó đó trong dấu nháy đôi

Ví dụ 1: Tâng xúc xắc
/nsr_bot roll_dice 1 6
-> Kết quả là: 6

Ví dụ 2: Chọn 1 trong các câu
/nsr_bot pick Neon Brim Chamber "Trần Tây"
-> Chọn: Trần Tây

Để xem danh sách động từ, sử dụng câu lệnh "/nsr_bot all_action"
"""

ALL_ACTIONS = """
1. roll_dice <số nhỏ nhất> <số lớn nhất> (chọn 1 số NGUYÊN bất kỳ trong khoảng, nếu không cung cấp khoảng thì mặc định là từ 1 đến 6)
VD: /nsr_bot roll_dice 1 6 
-> Kết quả là: 5

2. pick <danh sách lựa chọn> (chọn 1 cái trong danh sách)
VD: /nsr_bot pick Brim Kéo Búa "Trần Tây"
-> Chọn: Trần Tây

3. pick_team_vlr <loại team> <danh sách các thành viên>\n
    <loại team>
        std (tiêu chuẩn: 1 duelist, 1 init, 1 controller, 1 sentinels, 1 role bất kỳ)
        meme (chọn bất kỳ luôn :3 )
        rush (toàn duelist, không có gắn số lùi)
        smoke (chỉ có smoke, an toàn là trên hết)
        blind (chỉ có flash, nhắm mắt lại mà bắn)
        sen (chỉ có sentinels, trạm kiểm soát đây, đố team bạn rush được)

Nếu danh sách thành viên không cung cấp hoặc cung cấp đủ/thừa thì mặc định sẽ pick ra 5 agents

VD: /nsr_bot pick_team_vlr meme Tây Khang Nhím Nhân Huy
-> Tây: Phoenix
   Khang: Neon
   Nhím: Yoru
   Nhân: Chamber
   Huy: Cypher

4. help (in ra bảng hướng dẫn sử dụng)
5. all_action (in ra bảng động từ)
"""

ORIGINAL_PARAMETERS = {}
VALORANT_AGENTS = [
    "Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher", "Deadlock",
    "Fade", "Gekko", "Harbor", "Iso", "Jett", "KAY/O", "Killjoy", "Neon",
    "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", "Viper", "Yoru"
]

VALORANT_AGENTS_CATEGORY = {
    "duelist": ["Phoenix", "Jett", "Reyna", "Raze", "Yoru", "Neon"],
    "initiator": ["Sova", "Breach", "Skye", "KAY/O", "Fade", "Gekko"],
    "controller": ["Brimstone", "Omen", "Viper", "Astra", "Harbor"],
    "sentinels": ["Sage", "Cyper", "Killjoy", "Chamber", "Deadlock"],
    "flash": ["Phoenix", "Yoru", "Reyna", "Skye", "Breach", "KAY/O"],
    "smoke":
    ["Brimstone", "Omen", "Viper", "Astra", "Harbor", "Jett", "Cypher"]
}


def roll_dice(min_num=1, max_num=6) -> str:
    return f"Kết quả là {randint(min_num, max_num)}"


def pick(choices: list) -> str:
    return f"Chọn: {choice(choices)}"


def pick_random_and_remove(lst: list):
    random_pick = choice(lst)
    lst.remove(random_pick)
    return random_pick


def pick_team_vlr(category: str, members: list) -> str:
    agents_picked_list = []
    category_to_agent_category = {
        "rush": "duelist",
        "smoke": "smoke",
        "blind": "flash",
        "sen": "sentinels",
    }

    if category == "std":
        # Standard: Ensure one agent from each role
        agents_picked_list.append(choice(VALORANT_AGENTS_CATEGORY["duelist"]))
        agents_picked_list.append(choice(
            VALORANT_AGENTS_CATEGORY["initiator"]))
        agents_picked_list.append(
            choice(VALORANT_AGENTS_CATEGORY["controller"]))
        agents_picked_list.append(choice(
            VALORANT_AGENTS_CATEGORY["sentinels"]))
        agents_picked_list.append(choice(VALORANT_AGENTS_CATEGORY["flash"]))
    elif category == "meme":
        # Meme: Random agents from all
        agents_picked_list = sample(VALORANT_AGENTS, k=5)
    elif category in category_to_agent_category:
        # Category-specific: Unique agents
        agent_pool = VALORANT_AGENTS_CATEGORY[
            category_to_agent_category[category]]
        if len(agent_pool) < 5:
            return "Không đủ agent trong loại này để tạo team."
        agents_picked_list = sample(agent_pool, k=5)
    else:
        return f"Không tìm thấy loại team {category}"

    # Ensure we have 5 members
    while len(members) < 5:
        members.append(f"Thành viên {len(members) + 1}")

    final_str = "\n".join(
        f"{player}: {agent}"
        for player, agent in zip(members, agents_picked_list))
    return final_str


def get_response(user_input: str) -> str:
    original_string = user_input
    original_tokens = shlex.split(original_string)

    lowered_str = user_input.lower()
    split_tokens = shlex.split(lowered_str)

    for i, j in zip(split_tokens, original_tokens):
        ORIGINAL_PARAMETERS[i] = j

    if len(split_tokens) == 0:
        return 'Dùng câu lệnh "/nsr_bot help" để đọc hướng dẫn sử dụng'

    if split_tokens[0] == "help":
        return HELP_MESSAGE

    if split_tokens[0] == "all_action":
        return ALL_ACTIONS
    if split_tokens[0] == "quantronglagi?":
        return "Quan trọng là tốc độ"
    if split_tokens[0] == "aideptrainhat":
        return "Anh nhím"
    if split_tokens[0] == "good_bot":
        return "hehe"
    if split_tokens[0] == "roll_dice":
        if len(split_tokens) == 3:
            try:
                min_num = int(split_tokens[1])
                max_num = int(split_tokens[2])
                print(min_num, max_num)
                return roll_dice(min_num, max_num)
            except ValueError:
                return "Số cung cấp không hợp lệ!"
        return roll_dice()

    if split_tokens[0] == "pick":
        nouns = original_tokens[1:]
        return pick(nouns)

    if split_tokens[1] == "pick_team_vlr":
        if len(split_tokens) < 2:
            return 'Cần cung cấp loại team. Dùng "/nsr_bot all_action" để xem hướng dẫn.'
        category = split_tokens[1]
        members = original_tokens[2:] if len(original_tokens) > 3 else []
        return pick_team_vlr(category, members)




    return f'Không tìm thấy động từ {split_tokens[0]}, dùng câu lệnh "/nsr_bot all_action" để in ra các động từ'
