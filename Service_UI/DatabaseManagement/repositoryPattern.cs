using Microsoft.EntityFrameworkCore;

namespace WSDRA
{
    // IRepository interface
    public interface repositoryPattern<dataTableClass> where dataTableClass : class
    {
        dataTableClass GetById(int id);
        void AddSample(dataTableClass entity);
        void UpdateSample(dataTableClass entity);
        void DeleteSample(dataTableClass entity);

        void Save();
    }

    // Generic repository class implementing IRepository
    public class Repository<dataTableClass> : repositoryPattern<dataTableClass> where dataTableClass : class
    {
        private DRADbContext dbContext;

        public Repository(DRADbContext dbContext)
        {
            this.dbContext = dbContext;
        }

        public dataTableClass GetById(int id)
        {
            return dbContext.Set<dataTableClass>().Find(id);
        }

        // works
        public void AddSample(dataTableClass entity)
        {
            dbContext.Set<dataTableClass>().Add(entity);
            Save();
        }

        //
        public void UpdateSample(dataTableClass entity)
        {
            dbContext.Set<dataTableClass>().Update(entity);
        }

        // works
        public void DeleteSample(dataTableClass entity)
        {
            dbContext.Set<dataTableClass>().Remove(entity);
        }

        public void Save()
        {
            dbContext.SaveChanges();
        }
    }
}
