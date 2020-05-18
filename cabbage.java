import java.io.*;
import java.util.*;
/*
 Minjune Kim
 G Block
 Mr.Harris
 1/24/20
 */

public class cabbage {
	
	private static void sentence_remove_multiple(String[] sentence) {
		int counter =0;
		for(int i = 0; i < sentence.length; i++) {
			if(i == sentence.length -1) {
				System.out.println(counter + " " + sentence[i]);
			}
			else if(!sentence[i].equals(sentence[i+1])) {
				System.out.println(counter + " " + sentence[i]);
				counter++;
			}
			
		}
	}
	
	private static String[] sentence_organize(String[] sentence) {
		Arrays.sort(sentence);
		return sentence;
	}
	
	private static String[] sentence_lowercase(String[] sentence) {
		for(int i =0; i < sentence.length; i++) {
			sentence[i] = sentence[i].toLowerCase();
		}
		return sentence;
	}
	
	private static String[] sentence_cut(String[] sentences) {
		int counter = 0;
		for(int i = 0; i < sentences.length; i++) {
			if(sentences[i] == null) {
				counter = i;
				break;
			}
		}
		String[] sentence = new String[counter];
		for(int i = 0; i < sentence.length; i++) {
			sentence[i] = sentences[i];
		}
		return sentence;
	}
	
	private static String[] sentence(String word, String[] sentence, int counter) {
		sentence[counter-1] = word;
		return sentence;
	}
	
	private static String punctuation_remover(String word) {
		int length = word.length();
		String words = "!";
		for(int i = 0; i < length; i++) {
			String word1 = word.substring(i, i+1);
			if(word1.compareTo(words) < 32 || (word1.compareTo(words) < 64 && word1.compareTo(words) > 57) || (word1.compareTo(words) > 89)){
				word = word.replace(word1, " ");
			}
		}
		word = word.trim();
		for(int i = 0; i < word.length(); i++) {
			if(word.charAt(i) == ' ') {
				word = word.replace(" ", "");
			}
		}
		return word;
	}
	
	private static String display(int counter, String word, String words) {
		System.out.println(counter + " " + word);
		if(word.length() > words.length()) {
			words = word;
		}
		return words;
	}
	
	private static void grep(String[] sentences, String grep) {
		int[] sentence_length = new int[sentences.length];
		int sum = 0;
		int total = 0; 
		int index = 0;
		int index_1 = 0;
		int index_2 = 0;
		int counter = 0;
		int length = grep.length();
		for(int i = 0; i < sentences.length; i++) {
			sentence_length[i] = sentences[i].length();
		}
		
		String paragraph = sentences[0];
		
		for(int i = 1; i < sentences.length; i++) {
			paragraph = paragraph.concat(sentences[i]);
		}
		index = paragraph.indexOf(grep);
		index_2 = index;
		while(index != -1) {
		if(counter != 0)
			index = index_1;
		index_1 = index;
		int total1 = 0;
		for(int j = 0; j < sentences.length; j++) {
			if(sum + sentence_length[j] > index) {
				total1 = sum;
				sum = j;
				break;
			}
			sum += sentence_length[j];
		}
		int total2 = 0;
		for(int k = 0; k < sentences.length; k++) {
			if(total + sentence_length[k] > index + length) {
				total2 = total;
				total = k;
				break;
			}
			total += sentence_length[k];
		}
		int location = index - total1;
		int location2 = index + length -total2;
		if(location + length <= sentence_length[sum]) {
			System.out.println("Line " + (sum+1)  + " " + sentences[sum].substring(0, location) + "<" + grep + ">" + sentences[sum].substring(location + length, sentence_length[sum]));
		}
		else {
			System.out.println("Line " + (sum+1) + " " + sentences[sum].substring(0, location) + "<" + sentences[sum].substring(location, sentence_length[sum]));
			sum++;
			while(total - sum != 0) {
				System.out.println("Line " + (sum+1) + " " + sentences[sum]);
				sum++;
			}
			System.out.println("Line " + (sum + 1) + " " + sentences[total].substring(0, location2) + ">" + sentences[sum].substring(location2, sentence_length[total]));
		}
		if(index_2 + length < paragraph.length()) {
			paragraph = paragraph.substring((index_2 + length), paragraph.length());
		}
		else {
			paragraph = paragraph.substring(length + index_2, paragraph.length());
		}
		index = paragraph.indexOf(grep);
		index_1 = index_1 + index + length;
		index_2 = index;
		sum = 0;
		total = 0;
		counter++;
		}
		if(index == -1 && counter == 0) {
			System.out.println("Index is not found");
		}
	}
	
	public static void main (String[] args) {
		String pathname = "Cabbages (1).txt";
		File file = new File(pathname);
		Scanner input = null;
		Scanner reader = new Scanner(System.in);
		int counter = 0;
		String word = " ";
		String word1 = " ";
		try {
			input = new Scanner(file);
		}
		catch(FileNotFoundException ex) {
			System.out.println("*** Cannot open " + pathname + "***");
			System.exit(1);
		}
		System.out.println("Words found in text --");
		while(input.hasNext()) { 
			String num = input.next();
			word1 = num;
			counter ++;
			word = display(counter, num, word);
			
		}
		String[] sentence = new String[counter];
		counter = 0;
		try {
			input = new Scanner(file);
		}
		catch(FileNotFoundException ex) {
			System.out.println("*** Cannot open " + pathname + "***");
			System.exit(1);
		}
		while(input.hasNext()) {
			String num = input.next();
			word1 = num;
			word1 = punctuation_remover(word1);
			counter++;
			sentence = sentence(word1, sentence, counter);
		}
		input.close();
		System.out.println("The longest word in the text is <" + word + ">");
		sentence = sentence_lowercase(sentence);
		sentence = sentence_organize(sentence);
		System.out.println("Words sorted alphabetically with duplicates removed -- ");
		sentence_remove_multiple(sentence);
		String[] sentences = new String[counter];
		counter = 0;
		try {
			input = new Scanner(file);
		}
		catch(FileNotFoundException ex) {
			System.out.println("*** Cannot open " + pathname + "***");
			System.exit(1);
		}
		while(input.hasNextLine()) {
			String num = input.nextLine();
			counter++;
			sentences = sentence(num, sentences, counter);
		}
		System.out.println("Please enter something to grep: ");
		String grep = reader.nextLine();
		sentences = sentence_cut(sentences);
		grep(sentences, grep);
		System.out.println("Please enter something to grep: ");
		String grep1 = reader.nextLine();
		grep(sentences, grep1);
		System.out.println("Please enter something to grep: ");
		String grep2 = reader.nextLine();
		grep(sentences, grep2);
		input.close();
	}
	
}
