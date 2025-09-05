// 2. Frequency check
freq[letters.length-1] = correctLength - freq[0]; 
for (int i = 1; i < letters.length - 1; i++) { // Cost = c1; Occurences = 4
    String guess = String.valueOf(letters[i]).repeat(correctLength); // Cost = c2; Occurences = 4
    freq[i] = code.guess(guess); // Cost = c3; Occurences = 4 x L 
    freq[letters.length-1] -= freq[i]; // Cost = c4; Occurences = 4 
    if (freq[i] == correctLength) { // Cost = c5; Occrences = 4
        System.out.println("I found the secret code. It is " + guess);  // Cost = c6; Occurences = 4 
        return;
    }
    
}