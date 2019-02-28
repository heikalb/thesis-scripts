import java.util.List;
import zemberek.morphology.TurkishMorphology;
import zemberek.core.logging.Log;
import zemberek.morphology.analysis.SentenceAnalysis;
import zemberek.morphology.analysis.SingleAnalysis;
import zemberek.morphology.analysis.WordAnalysis;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.io.FileWriter;
import java.io.File;

public class ParseMorphemes
{
    public static void main (String[] args) throws IOException
    {
        // Corpus file
        FileReader fileReader = new FileReader("../data/query_results_all_joined_sents.tsv");
        BufferedReader br = new BufferedReader(fileReader);

        // For Turkish morphological processing
        TurkishMorphology morphology = TurkishMorphology.createWithDefaults();

        // Go through lines in file
        String line;
        while ((line = br.readLine()) != null)
        {

        }

        String sentence = "Bol baharatlı bir yemek yaptıralım.";
        List<WordAnalysis> analyses = morphology.analyzeSentence(sentence);
        SentenceAnalysis result = morphology.disambiguate(sentence, analyses);

        Log.info("\nAfter ambiguity resolution : ");
        result.bestAnalysis().forEach(Log::info);

        System.exit(0);
    }
}
