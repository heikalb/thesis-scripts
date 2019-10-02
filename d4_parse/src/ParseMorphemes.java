/**
 * Get morphological parses on TNC data.
 * Heikal Badrulhisham <heikal93@gmail.com>, 2019
 */

import java.util.List;
import zemberek.morphology.TurkishMorphology;
import zemberek.morphology.analysis.SentenceAnalysis;
import zemberek.morphology.analysis.WordAnalysis;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.io.FileWriter;
import java.io.File;

public class ParseMorphemes
{
    public static void main(String[] args) throws IOException
    {
        /**
         * Perform morphological parses on words in sentences in preprocessed
         * TNC data file for all verb stems. Save parses in another set of files
         * for all verb stems.
         */
        // Files of TNC query results by verbs
        File[] queryFiles = new File("../d2_data/joined/").listFiles();

        // Process each file
        for(File f: queryFiles)
        {
            // Read the content of the file
            String dataFile = f.getName();
            FileReader fileReader = new FileReader("../d2_data/joined/" + dataFile);
            BufferedReader reader = new BufferedReader(fileReader);

            // Turkish morphological parser
            TurkishMorphology parser = TurkishMorphology.createWithDefaults();

            // For collecting parses
            ArrayList<List> parses = new ArrayList();

            // Go through lines in file
            String line;

            while ((line = reader.readLine()) != null)
            {
                // Get words in sentence as list
                String sentence = line.split("\t")[0];
                // Get morphological parses for each word in sentence
                List<WordAnalysis> analyses = parser.analyzeSentence(sentence);
                // Disambiguate between multiple parses
                SentenceAnalysis finalAnalysis = parser.disambiguate(sentence, analyses);
                // Collect best parse
                parses.add(finalAnalysis.bestAnalysis());
            }

            // Save data
            String fileIndex = dataFile.split("_")[0];
            String fileStem = dataFile.split("_")[1];
            String path = "parses/" + fileIndex + "_" + fileStem + "_parses.txt";
            File saveFile = new File(path);
            FileWriter writer = new FileWriter(saveFile);

            for(List parseList: parses)
                writer.append(parseList.toString() + '\n');

            writer.flush();
            writer.close();
        }
    }
}
