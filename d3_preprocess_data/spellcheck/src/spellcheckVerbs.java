/*
Collect verbs from the subcorpus with a spelling error and save spelling correction suggestions
Heikal Badrulhisham <heikal93@gmail.com>, 2019
 */

import zemberek.morphology.TurkishMorphology;
import zemberek.normalization.TurkishSpellChecker;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.io.FileWriter;
import java.io.File;

public class spellcheckVerbs
{
    public static void main(String[] args) throws IOException
    {
        // Zemberek NLP spellchecker
        TurkishMorphology morphology = TurkishMorphology.createWithDefaults();
        TurkishSpellChecker spellChecker = new TurkishSpellChecker(morphology);

        // File of verbs
        FileReader fileReader = new FileReader("../../data/all_verbs.txt");
        BufferedReader br = new BufferedReader(fileReader);

        // For keeping track of words that have already been processed
        ArrayList<String> misspelledWords = new ArrayList<>();
        // Store spelling corrections to avoid processing the same words again
        ArrayList error_corrections = new ArrayList<>();

        // Go through lines of verb file
        String st;
        while ((st = br.readLine()) != null)
        {
            // Get correction if there's an error (hitherto non-encountered words only)
            if (!spellChecker.check(st) && !misspelledWords.contains(st))
            {
                misspelledWords.add(st);
                List<String> correction = spellChecker.suggestForWord(st);
                // Workaround for a type-related issue
                String[] correction_ = correction.toArray(new String[correction.size()]);
                String output = st + " " + String.join(" ", correction_);
                error_corrections.add(output);
            }
        }

        // Save data
        FileWriter fr = new FileWriter(new File("../../data/verb_spellcheck.txt"));
        fr.write(String.join("\n", error_corrections));

        // Fin
        System.exit(0);
    }
}
